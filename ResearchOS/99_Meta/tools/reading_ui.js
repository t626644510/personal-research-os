const ReadingWorkspaceModel = (() => {
  "use strict";

  const FORMAT_VERSION = "rw-session-v0.1";
  const SESSION_ENVELOPE_PATTERN = "^[ \\t]*<!--[ \\t]*rw-session-v0\\.1[ \\t]*-->[ \\t]*\\r?\\n[ \\t]*```json[ \\t]*\\r?\\n([\\s\\S]*?)\\r?\\n[ \\t]*```[ \\t]*(?:\\r?\\n|$)";
  const SESSION_TAB_ENTRY_TYPES = Object.freeze({
    excerpts: Object.freeze(["source_excerpt"]),
    notes: Object.freeze(["human_note"]),
    qa: Object.freeze(["human_question", "llm_answer"]),
    all: null,
  });
  const SESSION_PANEL_WIDTHS = Object.freeze({
    compact: "34rem",
    balanced: "42rem",
    wide: "50rem",
  });
  const DEFAULT_SESSION_PANEL_WIDTH = "balanced";
  const SELECTED_TEXT_ORIGINS = Object.freeze({
    authoritative: "authoritative_source",
    translation: "reference_translation",
  });
  const OPTIONAL_SELECTION_FIELDS = Object.freeze([
    "selected_text_origin",
    "selected_block_id",
  ]);
  const ANNOTATABLE_ENTRY_TYPES = new Set([
    "source_excerpt",
    "human_note",
    "human_question",
  ]);
  const DEFAULT_PRESENTATION_LAYOUT = Object.freeze({
    language_ratio: 0.5,
    figures_width_rem: 28,
    session_width_rem: 42,
    session_width_preset: DEFAULT_SESSION_PANEL_WIDTH,
  });
  const PRESENTATION_LIMITS = Object.freeze({
    language_min_px: 240,
    body_min_px: 544,
    figures_min_px: 288,
    session_min_px: 384,
    separator_width_px: 8,
  });

  function normalizeSessionPanelWidth(value) {
    return Object.prototype.hasOwnProperty.call(SESSION_PANEL_WIDTHS, value)
      ? value
      : DEFAULT_SESSION_PANEL_WIDTH;
  }

  function selectedTextOrigin(entry) {
    return Object.prototype.hasOwnProperty.call(entry, "selected_text_origin")
      ? entry.selected_text_origin
      : SELECTED_TEXT_ORIGINS.authoritative;
  }

  function selectionFieldSnapshot(entry) {
    const snapshot = {};
    OPTIONAL_SELECTION_FIELDS.forEach((field) => {
      if (Object.prototype.hasOwnProperty.call(entry, field)) {
        snapshot[field] = entry[field];
      }
    });
    return snapshot;
  }

  function validateSelectionFields(entry, linkedQuestion = null) {
    const hasOrigin = Object.prototype.hasOwnProperty.call(entry, "selected_text_origin");
    const hasBlockId = Object.prototype.hasOwnProperty.call(entry, "selected_block_id");
    if (hasOrigin && !Object.values(SELECTED_TEXT_ORIGINS).includes(entry.selected_text_origin)) {
      throw new Error(`selected_text_origin 无效：${entry.entry_id || "(未知条目)"}`);
    }
    if (
      hasBlockId &&
      (typeof entry.selected_block_id !== "string" || !entry.selected_block_id.trim())
    ) {
      throw new Error(`selected_block_id 必须是非空字符串：${entry.entry_id || "(未知条目)"}`);
    }

    const origin = selectedTextOrigin(entry);
    if (
      origin === SELECTED_TEXT_ORIGINS.translation &&
      !["human_note", "human_question", "llm_answer"].includes(entry.entry_type)
    ) {
      throw new Error(`中文参考译文不能创建 ${entry.entry_type}：${entry.entry_id || "(未知条目)"}`);
    }
    if (entry.entry_type === "source_excerpt" && origin !== SELECTED_TEXT_ORIGINS.authoritative) {
      throw new Error(`中文参考译文不能创建 source_excerpt：${entry.entry_id || "(未知条目)"}`);
    }
    if (entry.entry_type === "llm_answer" && linkedQuestion) {
      const questionOrigin = selectedTextOrigin(linkedQuestion);
      if (origin !== questionOrigin) {
        throw new Error(`LLM 回答必须继承问题的选区来源：${entry.entry_id || "(未知条目)"}`);
      }
    }
    return origin;
  }

  function normalizeAnnotationText(value) {
    return String(value || "").normalize("NFC").replace(/\s+/g, " ").trim();
  }

  function resolveBlockAnnotations(entries, blocks) {
    const blockCounts = {};
    let unlocatedCount = 0;
    entries.forEach((entry) => {
      if (!ANNOTATABLE_ENTRY_TYPES.has(entry.entry_type)) return;
      const origin = selectedTextOrigin(entry);
      const originBlocks = blocks.filter((block) => block.source_origin === origin);
      const selectedText = normalizeAnnotationText(entry.selected_text);
      const matchesEntry = (block) =>
        Boolean(selectedText) &&
        block.source_locator === entry.source_locator &&
        normalizeAnnotationText(block.visible_text).includes(selectedText);
      let matches;
      if (Object.prototype.hasOwnProperty.call(entry, "selected_block_id")) {
        const verifiedIdMatches = originBlocks.filter(
          (block) => block.block_id === entry.selected_block_id && matchesEntry(block),
        );
        matches =
          verifiedIdMatches.length === 1
            ? verifiedIdMatches
            : originBlocks.filter(matchesEntry);
      } else {
        matches = originBlocks.filter(matchesEntry);
      }
      if (matches.length !== 1) {
        unlocatedCount += 1;
        return;
      }
      const blockKey = String(matches[0].block_key ?? matches[0].block_id);
      blockCounts[blockKey] = (blockCounts[blockKey] || 0) + 1;
    });
    return { blockCounts, unlocatedCount };
  }

  function finiteNumber(value, fallback) {
    return typeof value === "number" && Number.isFinite(value) ? value : fallback;
  }

  function normalizePresentationLayout(value) {
    const source = value && typeof value === "object" && !Array.isArray(value) ? value : {};
    const preset = ["compact", "balanced", "wide", "custom"].includes(
      source.session_width_preset,
    )
      ? source.session_width_preset
      : DEFAULT_PRESENTATION_LAYOUT.session_width_preset;
    const presetWidth = SESSION_PANEL_WIDTHS[preset]
      ? Number.parseFloat(SESSION_PANEL_WIDTHS[preset])
      : null;
    const normalized = {
      language_ratio: Math.min(
        0.95,
        Math.max(0.05, finiteNumber(source.language_ratio, DEFAULT_PRESENTATION_LAYOUT.language_ratio)),
      ),
      figures_width_rem: Math.min(
        120,
        Math.max(8, finiteNumber(source.figures_width_rem, DEFAULT_PRESENTATION_LAYOUT.figures_width_rem)),
      ),
      session_width_rem: Math.min(
        120,
        Math.max(8, finiteNumber(source.session_width_rem, DEFAULT_PRESENTATION_LAYOUT.session_width_rem)),
      ),
      session_width_preset: preset,
    };
    if (presetWidth !== null) normalized.session_width_rem = presetWidth;
    return normalized;
  }

  function clampPresentationLayout(value, metrics = {}) {
    const layout = normalizePresentationLayout(value);
    const rootFontPx = Math.max(1, finiteNumber(metrics.rootFontPx, 16));
    const workspaceWidthPx = finiteNumber(metrics.workspaceWidthPx, 0);
    const bodyWidthPx = finiteNumber(metrics.bodyWidthPx, 0);
    const separatorWidthPx = Math.max(
      0,
      finiteNumber(metrics.separatorWidthPx, PRESENTATION_LIMITS.separator_width_px),
    );
    if (workspaceWidthPx > 800) {
      const usableWidth = workspaceWidthPx - separatorWidthPx * 2;
      const maximumSession = Math.max(
        PRESENTATION_LIMITS.session_min_px,
        usableWidth - PRESENTATION_LIMITS.body_min_px - PRESENTATION_LIMITS.figures_min_px,
      );
      let sessionWidthPx = Math.min(
        maximumSession,
        Math.max(PRESENTATION_LIMITS.session_min_px, layout.session_width_rem * rootFontPx),
      );
      const maximumFigures = Math.max(
        PRESENTATION_LIMITS.figures_min_px,
        usableWidth - PRESENTATION_LIMITS.body_min_px - sessionWidthPx,
      );
      let figuresWidthPx = Math.min(
        maximumFigures,
        Math.max(PRESENTATION_LIMITS.figures_min_px, layout.figures_width_rem * rootFontPx),
      );
      if (figuresWidthPx + sessionWidthPx + PRESENTATION_LIMITS.body_min_px > usableWidth) {
        sessionWidthPx = Math.max(
          PRESENTATION_LIMITS.session_min_px,
          usableWidth - PRESENTATION_LIMITS.body_min_px - figuresWidthPx,
        );
      }
      layout.figures_width_rem = Number((figuresWidthPx / rootFontPx).toFixed(3));
      layout.session_width_rem = Number((sessionWidthPx / rootFontPx).toFixed(3));
    }
    if (bodyWidthPx > 0) {
      const languageWidth = Math.max(1, bodyWidthPx - separatorWidthPx);
      const minimumRatio = Math.min(0.5, PRESENTATION_LIMITS.language_min_px / languageWidth);
      layout.language_ratio = Math.min(
        1 - minimumRatio,
        Math.max(minimumRatio, layout.language_ratio),
      );
    }
    return layout;
  }

  function resizePresentationLayout(value, handle, deltaPx, metrics = {}) {
    const layout = clampPresentationLayout(value, metrics);
    const rootFontPx = Math.max(1, finiteNumber(metrics.rootFontPx, 16));
    const deltaRem = finiteNumber(deltaPx, 0) / rootFontPx;
    if (handle === "language") {
      const bodyWidthPx = Math.max(1, finiteNumber(metrics.bodyWidthPx, 1));
      const separatorWidthPx = Math.max(
        0,
        finiteNumber(metrics.separatorWidthPx, PRESENTATION_LIMITS.separator_width_px),
      );
      const usableWidth = Math.max(1, bodyWidthPx - separatorWidthPx);
      layout.language_ratio = (layout.language_ratio * usableWidth + deltaPx) / usableWidth;
    } else if (handle === "figures") {
      layout.figures_width_rem -= deltaRem;
    } else if (handle === "session") {
      const totalRailWidth = layout.figures_width_rem + layout.session_width_rem;
      const minimumFiguresRem = PRESENTATION_LIMITS.figures_min_px / rootFontPx;
      const minimumSessionRem = PRESENTATION_LIMITS.session_min_px / rootFontPx;
      const workspaceWidthPx = finiteNumber(metrics.workspaceWidthPx, 0);
      const separatorWidthPx = Math.max(
        0,
        finiteNumber(metrics.separatorWidthPx, PRESENTATION_LIMITS.separator_width_px),
      );
      const maximumRailWidth = workspaceWidthPx > 800
        ? (workspaceWidthPx - separatorWidthPx * 2 - PRESENTATION_LIMITS.body_min_px) / rootFontPx
        : totalRailWidth;
      const clampedRailWidth = Math.max(
        minimumFiguresRem + minimumSessionRem,
        Math.min(totalRailWidth, maximumRailWidth),
      );
      layout.session_width_rem = Math.min(
        clampedRailWidth - minimumFiguresRem,
        Math.max(minimumSessionRem, layout.session_width_rem - deltaRem),
      );
      layout.figures_width_rem = clampedRailWidth - layout.session_width_rem;
      layout.session_width_preset = "custom";
    } else {
      throw new Error(`Unknown presentation resizer: ${handle}`);
    }
    return clampPresentationLayout(layout, metrics);
  }

  function presentationLayoutForPreset(value, preset) {
    const normalizedPreset = normalizeSessionPanelWidth(preset);
    const layout = normalizePresentationLayout(value);
    layout.session_width_preset = normalizedPreset;
    layout.session_width_rem = Number.parseFloat(SESSION_PANEL_WIDTHS[normalizedPreset]);
    return layout;
  }

  function entriesForTab(entries, tabName) {
    if (!Object.prototype.hasOwnProperty.call(SESSION_TAB_ENTRY_TYPES, tabName)) {
      throw new Error(`Unknown session tab: ${tabName}`);
    }
    const entryTypes = SESSION_TAB_ENTRY_TYPES[tabName];
    return entryTypes === null
      ? entries.slice()
      : entries.filter((entry) => entryTypes.includes(entry.entry_type));
  }

  function groupQuestionAnswers(entries) {
    const groups = entries
      .filter((entry) => entry.entry_type === "human_question")
      .map((question) => ({ question, answers: [] }));
    const groupsByQuestionId = new Map(
      groups.map((group) => [group.question.entry_id, group]),
    );
    entries.forEach((entry) => {
      if (entry.entry_type !== "llm_answer") return;
      const group = groupsByQuestionId.get(entry.question_entry_id);
      if (group) group.answers.push(entry);
    });
    return groups;
  }

  function buildSessionMarkdownEnvelope(payload) {
    return [
      "# Reading Workspace Session",
      "",
      `- Format: ${FORMAT_VERSION}`,
      `- Source: ${payload.source_label}`,
      `- Session state: ${payload.session_state}`,
      `- Exported at: ${payload.exported_at}`,
      "",
      "The fenced JSON block is the authoritative lossless session payload.",
      "",
      `<!-- ${FORMAT_VERSION} -->`,
      "```json",
      JSON.stringify(payload, null, 2),
      "```",
      "",
    ].join("\n");
  }

  function parseSessionMarkdownEnvelope(markdown) {
    const marker = new RegExp(SESSION_ENVELOPE_PATTERN, "im");
    const match = marker.exec(markdown);
    if (!match) throw new Error("未找到 rw-session-v0.1 JSON 数据块。");
    try {
      return JSON.parse(match[1]);
    } catch (error) {
      throw new Error(`会话 JSON 无效：${error.message}`);
    }
  }

  return Object.freeze({
    formatVersion: FORMAT_VERSION,
    sessionPanelWidths: SESSION_PANEL_WIDTHS,
    defaultSessionPanelWidth: DEFAULT_SESSION_PANEL_WIDTH,
    normalizeSessionPanelWidth,
    selectedTextOrigins: SELECTED_TEXT_ORIGINS,
    defaultPresentationLayout: DEFAULT_PRESENTATION_LAYOUT,
    presentationLimits: PRESENTATION_LIMITS,
    selectedTextOrigin,
    selectionFieldSnapshot,
    validateSelectionFields,
    normalizeAnnotationText,
    resolveBlockAnnotations,
    normalizePresentationLayout,
    clampPresentationLayout,
    resizePresentationLayout,
    presentationLayoutForPreset,
    entriesForTab,
    groupQuestionAnswers,
    buildSessionMarkdownEnvelope,
    parseSessionMarkdownEnvelope,
  });
})();

if (typeof module === "object" && module.exports) {
  module.exports = ReadingWorkspaceModel;
}

if (typeof document !== "undefined") {
(() => {
  "use strict";

  const bootstrapNode = document.getElementById("rw-bootstrap");
  const BOOTSTRAP = JSON.parse(bootstrapNode.textContent);
  const FORMAT_VERSION = ReadingWorkspaceModel.formatVersion;
  const AUTHOR_BY_ENTRY_TYPE = Object.freeze(BOOTSTRAP.author_by_entry_type);
  const ENTRY_DEFAULTS = Object.freeze(BOOTSTRAP.defaults);
  const ENTRY_TYPES = new Set(Object.keys(AUTHOR_BY_ENTRY_TYPE));
  const CONFIDENCE_VALUES = new Set(["not_assessed", "low", "medium", "high"]);
  const VERIFICATION_VALUES = new Set([
    "not_applicable",
    "unverified",
    "human_checked",
    "rejected",
  ]);
  const DENSITY_VALUES = new Set(["all", "paragraph", "section"]);
  const STORAGE_KEY = `personal-research-os:${BOOTSTRAP.session_id}`;
  const PRESENTATION_STORAGE_KEY =
    "personal-research-os:reading-workspace:presentation:v1";
  const SELECTED_TEXT_ORIGINS = ReadingWorkspaceModel.selectedTextOrigins;
  const TRANSLATION_PROVENANCE =
    "中文参考译文 / 机器或 LLM 辅助 / 未核验";
  const ENTRY_TYPE_LABELS = Object.freeze({
    source_excerpt: "来源摘录",
    human_note: "个人笔记",
    human_question: "人类问题",
    llm_answer: "LLM 回答",
  });

  const elements = {
    saveState: document.getElementById("save-state"),
    density: document.getElementById("density-control"),
    sessionPanelWidth: document.getElementById("session-panel-width"),
    highlightToggle: document.getElementById("highlight-toggle"),
    restoreMuted: document.getElementById("restore-muted"),
    exportSession: document.getElementById("export-session"),
    importSession: document.getElementById("import-session"),
    recoveryBanner: document.getElementById("recovery-banner"),
    recoverySummary: document.getElementById("recovery-summary"),
    recoverDraft: document.getElementById("recover-draft"),
    discardDraft: document.getElementById("discard-draft"),
    clearRecovery: document.getElementById("clear-recovery"),
    messageSurface: document.getElementById("message-surface"),
    selectionTools: document.getElementById("selection-tools"),
    selectionPreview: document.getElementById("selection-preview"),
    selectionOriginNote: document.getElementById("selection-origin-note"),
    selectionSourceExcerpt: document.getElementById("selection-source-excerpt"),
    annotationLocationStatus: document.getElementById("annotation-location-status"),
    referenceMode: document.getElementById("reference-mode"),
    referenceSurfaces: document.querySelector("[data-reference-surfaces]"),
    referencePanes: [...document.querySelectorAll("[data-reference-pane]")],
    figuresPanel: document.getElementById("figures-panel"),
    figuresSurface: document.getElementById("figures-surface"),
    workspaceShell: document.querySelector(".workspace-shell"),
    readerPane: document.querySelector(".reader-pane"),
    resetLayout: document.getElementById("reset-layout"),
    languageResizer: document.getElementById("language-resizer"),
    contentFiguresResizer: document.getElementById("content-figures-resizer"),
    figuresSessionResizer: document.getElementById("figures-session-resizer"),
    mutedSummary: document.getElementById("muted-summary"),
    sessionTabs: [...document.querySelectorAll("[data-session-tab]")],
    sessionList: document.getElementById("session-list"),
    entryCount: document.getElementById("entry-count"),
    addAnswer: document.getElementById("add-llm-answer"),
    entryDialog: document.getElementById("entry-dialog"),
    entryForm: document.getElementById("entry-form"),
    entryDialogType: document.getElementById("entry-dialog-type"),
    entryDialogTitle: document.getElementById("entry-dialog-title"),
    entryOrigin: document.getElementById("entry-origin"),
    entryLocator: document.getElementById("entry-locator"),
    entrySelectedText: document.getElementById("entry-selected-text"),
    entryContent: document.getElementById("entry-content"),
    answerDialog: document.getElementById("answer-dialog"),
    answerForm: document.getElementById("answer-form"),
    answerQuestion: document.getElementById("answer-question"),
    answerModelLabel: document.getElementById("answer-model-label"),
    answerContent: document.getElementById("answer-content"),
    packetDialog: document.getElementById("packet-dialog"),
    packetContent: document.getElementById("packet-content"),
    copyPacket: document.getElementById("copy-packet"),
  };
  const selectionRoots = [
    elements.referenceSurfaces,
    elements.figuresSurface,
  ].filter(Boolean);
  const resizers = [
    elements.languageResizer,
    elements.contentFiguresResizer,
    elements.figuresSessionResizer,
  ].filter(Boolean);

  let state = {
    entries: [],
    preferences: clone(BOOTSTRAP.initial_preferences),
  };
  let recoveryDraft = null;
  let currentSelection = null;
  let editingEntryId = null;
  let activeSessionTab = "all";
  let presentationLayout = clone(ReadingWorkspaceModel.defaultPresentationLayout);
  const REFERENCE_MODES = new Set(["english", "bilingual", "translation"]);

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function applyReferenceMode(value) {
    if (!elements.referenceMode) return "english";
    const normalized = REFERENCE_MODES.has(value) ? value : "bilingual";
    const showEnglish = normalized !== "translation";
    const showTranslation = normalized !== "english";
    elements.referenceMode.value = normalized;
    if (elements.referenceSurfaces) {
      elements.referenceSurfaces.dataset.referenceMode = normalized;
      elements.referenceSurfaces.classList.remove(
        "reference-mode-english",
        "reference-mode-bilingual",
        "reference-mode-translation",
      );
      elements.referenceSurfaces.classList.add(`reference-mode-${normalized}`);
    }
    elements.referencePanes.forEach((pane) => {
      const visible = pane.dataset.referencePane === "english" ? showEnglish : showTranslation;
      pane.hidden = !visible;
      pane.setAttribute("aria-hidden", String(!visible));
    });
    if (elements.languageResizer) {
      const visible = normalized === "bilingual";
      elements.languageResizer.hidden = !visible;
      elements.languageResizer.setAttribute("aria-hidden", String(!visible));
      elements.languageResizer.tabIndex = visible ? 0 : -1;
    }
    return normalized;
  }

  function createElement(tagName, className, text) {
    const node = document.createElement(tagName);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function setMessage(message, tone = "info") {
    elements.messageSurface.textContent = message;
    elements.messageSurface.dataset.tone = tone;
  }

  function setSaveState(kind, label) {
    elements.saveState.dataset.state = kind;
    elements.saveState.textContent = label;
  }

  function presentationMetrics() {
    const rootFontPx = Number.parseFloat(
      window.getComputedStyle(document.documentElement).fontSize,
    ) || 16;
    const workspaceWidthPx = elements.workspaceShell
      ? elements.workspaceShell.getBoundingClientRect().width
      : window.innerWidth;
    const bodyWidthPx = elements.readerPane
      ? elements.readerPane.getBoundingClientRect().width
      : workspaceWidthPx;
    const separatorWidthPx = elements.contentFiguresResizer
      ? elements.contentFiguresResizer.getBoundingClientRect().width || 8
      : 8;
    return { rootFontPx, workspaceWidthPx, bodyWidthPx, separatorWidthPx };
  }

  function ensureCustomWidthOption() {
    if (!elements.sessionPanelWidth) return;
    if (elements.sessionPanelWidth.querySelector('option[value="custom"]')) return;
    const option = document.createElement("option");
    option.value = "custom";
    option.textContent = "自定义";
    elements.sessionPanelWidth.append(option);
  }

  function updateResizerAccessibility(layout, metrics) {
    const rootFontPx = metrics.rootFontPx || 16;
    const workspaceRem = metrics.workspaceWidthPx / rootFontPx;
    const bodyWidth = Math.max(1, metrics.bodyWidthPx - metrics.separatorWidthPx);
    const minimumLanguageRatio = Math.min(
      0.5,
      ReadingWorkspaceModel.presentationLimits.language_min_px / bodyWidth,
    );
    if (elements.languageResizer) {
      elements.languageResizer.setAttribute("aria-valuemin", String(Math.round(minimumLanguageRatio * 100)));
      elements.languageResizer.setAttribute("aria-valuemax", String(Math.round((1 - minimumLanguageRatio) * 100)));
      elements.languageResizer.setAttribute("aria-valuenow", String(Math.round(layout.language_ratio * 100)));
      elements.languageResizer.setAttribute("aria-valuetext", `英文栏 ${Math.round(layout.language_ratio * 100)}%`);
    }
    if (elements.contentFiguresResizer) {
      elements.contentFiguresResizer.setAttribute("aria-valuemin", "18");
      elements.contentFiguresResizer.setAttribute(
        "aria-valuemax",
        String(Math.max(18, Math.round(workspaceRem - layout.session_width_rem - 34))),
      );
      elements.contentFiguresResizer.setAttribute("aria-valuenow", String(Math.round(layout.figures_width_rem)));
      elements.contentFiguresResizer.setAttribute("aria-valuetext", `图表栏 ${layout.figures_width_rem.toFixed(1)}rem`);
    }
    if (elements.figuresSessionResizer) {
      elements.figuresSessionResizer.setAttribute("aria-valuemin", "24");
      elements.figuresSessionResizer.setAttribute(
        "aria-valuemax",
        String(Math.max(24, Math.round(workspaceRem - layout.figures_width_rem - 34))),
      );
      elements.figuresSessionResizer.setAttribute("aria-valuenow", String(Math.round(layout.session_width_rem)));
      elements.figuresSessionResizer.setAttribute("aria-valuetext", `会话栏 ${layout.session_width_rem.toFixed(1)}rem`);
    }
  }

  function applyPresentationLayout(value) {
    ensureCustomWidthOption();
    let metrics = presentationMetrics();
    presentationLayout = ReadingWorkspaceModel.clampPresentationLayout(value, metrics);
    document.documentElement.style.setProperty(
      "--language-column-position",
      `${(presentationLayout.language_ratio * 100).toFixed(3)}%`,
    );
    document.documentElement.style.setProperty(
      "--figures-panel-width",
      `${presentationLayout.figures_width_rem}rem`,
    );
    document.documentElement.style.setProperty(
      "--session-panel-width",
      `${presentationLayout.session_width_rem}rem`,
    );
    metrics = presentationMetrics();
    presentationLayout = ReadingWorkspaceModel.clampPresentationLayout(
      presentationLayout,
      metrics,
    );
    document.documentElement.style.setProperty(
      "--language-column-position",
      `${(presentationLayout.language_ratio * 100).toFixed(3)}%`,
    );
    document.documentElement.style.setProperty(
      "--figures-panel-width",
      `${presentationLayout.figures_width_rem}rem`,
    );
    document.documentElement.style.setProperty(
      "--session-panel-width",
      `${presentationLayout.session_width_rem}rem`,
    );
    if (elements.sessionPanelWidth) {
      const customOption = elements.sessionPanelWidth.querySelector('option[value="custom"]');
      if (customOption) {
        customOption.disabled = presentationLayout.session_width_preset !== "custom";
      }
      elements.sessionPanelWidth.value = presentationLayout.session_width_preset;
      const selectedOption = elements.sessionPanelWidth.querySelector(
        `option[value="${presentationLayout.session_width_preset}"]`,
      );
      if (selectedOption) selectedOption.selected = true;
    }
    updateResizerAccessibility(presentationLayout, metrics);
    return presentationLayout;
  }

  function persistPresentationLayout(successMessage = "阅读布局已保存。") {
    try {
      localStorage.setItem(PRESENTATION_STORAGE_KEY, JSON.stringify(presentationLayout));
      setMessage(successMessage, "success");
      return true;
    } catch (error) {
      setMessage(`布局已在当前页面应用，但无法跨页面保存：${error.message}`, "error");
      return false;
    }
  }

  function setPresentationLayout(value, successMessage) {
    applyPresentationLayout(value);
    persistPresentationLayout(successMessage);
  }

  function restorePresentationLayout() {
    let storedValue = null;
    try {
      storedValue = localStorage.getItem(PRESENTATION_STORAGE_KEY);
    } catch (error) {
      applyPresentationLayout(ReadingWorkspaceModel.defaultPresentationLayout);
      setMessage(`无法读取布局偏好；当前使用默认布局。${error.message}`, "error");
      return;
    }
    if (storedValue === null) {
      applyPresentationLayout(ReadingWorkspaceModel.defaultPresentationLayout);
      return;
    }
    try {
      const parsed = JSON.parse(storedValue);
      applyPresentationLayout(parsed);
    } catch (error) {
      applyPresentationLayout(ReadingWorkspaceModel.defaultPresentationLayout);
      setMessage(`已忽略无效布局偏好；当前使用默认布局。${error.message}`, "info");
    }
  }

  function applySessionPanelPreset() {
    if (!elements.sessionPanelWidth || elements.sessionPanelWidth.value === "custom") return;
    const next = ReadingWorkspaceModel.presentationLayoutForPreset(
      presentationLayout,
      elements.sessionPanelWidth.value,
    );
    setPresentationLayout(
      next,
      `会话栏宽度已设为 ${elements.sessionPanelWidth.selectedOptions[0].textContent}。`,
    );
  }

  function resetPresentationLayout() {
    setPresentationLayout(
      ReadingWorkspaceModel.defaultPresentationLayout,
      "阅读布局已恢复：中英 50/50、图表栏 28rem、会话栏 Balanced 42rem。",
    );
  }

  function preferenceSnapshot() {
    return {
      density: state.preferences.density,
      highlights_enabled: state.preferences.highlights_enabled,
      muted_concepts: [...state.preferences.muted_concepts].sort((a, b) => a.localeCompare(b)),
      muted_terms: [...state.preferences.muted_terms].sort((a, b) => a.localeCompare(b)),
    };
  }

  function entrySnapshot(entry) {
    const snapshot = {
      entry_id: entry.entry_id,
      entry_type: entry.entry_type,
      created_at: entry.created_at,
      author_type: entry.author_type,
      source_locator: entry.source_locator,
      selected_text: entry.selected_text,
      content: entry.content,
      confidence: entry.confidence,
      verification: entry.verification,
    };
    Object.assign(snapshot, ReadingWorkspaceModel.selectionFieldSnapshot(entry));
    if (entry.entry_type === "llm_answer") {
      snapshot.question_entry_id = entry.question_entry_id;
      if (Object.prototype.hasOwnProperty.call(entry, "model_label")) {
        snapshot.model_label = entry.model_label;
      }
    }
    return snapshot;
  }

  function sessionPayload(timestampField) {
    const payload = {
      format_version: FORMAT_VERSION,
      source_label: BOOTSTRAP.source_label,
      session_id: BOOTSTRAP.session_id,
      session_state: "active",
      entries: state.entries.map(entrySnapshot),
      preferences: preferenceSnapshot(),
    };
    if (timestampField) payload[timestampField] = new Date().toISOString();
    return payload;
  }

  function assertObject(value, label) {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      throw new Error(`${label} 必须是对象。`);
    }
  }

  function assertAllowedKeys(value, allowed, label) {
    const unexpected = Object.keys(value).filter((key) => !allowed.has(key));
    if (unexpected.length) {
      throw new Error(`${label} 包含不支持的字段：${unexpected.join(", ")}`);
    }
  }

  function assertString(value, label) {
    if (typeof value !== "string") throw new Error(`${label} 必须是字符串。`);
  }

  function assertStringArray(value, label) {
    if (!Array.isArray(value) || value.some((item) => typeof item !== "string")) {
      throw new Error(`${label} 必须是字符串数组。`);
    }
    if (new Set(value).size !== value.length) {
      throw new Error(`${label} 不得包含重复值。`);
    }
  }

  function validatePreferences(preferences) {
    assertObject(preferences, "preferences");
    assertAllowedKeys(
      preferences,
      new Set(["density", "highlights_enabled", "muted_concepts", "muted_terms"]),
      "preferences",
    );
    if (!DENSITY_VALUES.has(preferences.density)) {
      throw new Error("preferences.density 无效。");
    }
    if (typeof preferences.highlights_enabled !== "boolean") {
      throw new Error("preferences.highlights_enabled 必须是布尔值。");
    }
    assertStringArray(preferences.muted_concepts, "preferences.muted_concepts");
    assertStringArray(preferences.muted_terms, "preferences.muted_terms");
  }

  function validateEntry(entry, entryIds) {
    assertObject(entry, "session entry");
    assertAllowedKeys(
      entry,
      new Set([
        "entry_id",
        "entry_type",
        "created_at",
        "author_type",
        "source_locator",
        "selected_text",
        "content",
        "confidence",
        "verification",
        "selected_text_origin",
        "selected_block_id",
        "question_entry_id",
        "model_label",
      ]),
      "session entry",
    );
    [
      "entry_id",
      "entry_type",
      "created_at",
      "author_type",
      "source_locator",
      "selected_text",
      "content",
      "confidence",
      "verification",
    ].forEach((field) => assertString(entry[field], `entry.${field}`));
    if (!entry.entry_id || entryIds.has(entry.entry_id)) {
      throw new Error(`entry_id 必须非空且唯一：${entry.entry_id || "(空)"}`);
    }
    entryIds.add(entry.entry_id);
    if (!ENTRY_TYPES.has(entry.entry_type)) {
      throw new Error(`不支持的 entry_type：${entry.entry_type}`);
    }
    ReadingWorkspaceModel.validateSelectionFields(entry);
    if (entry.author_type !== AUTHOR_BY_ENTRY_TYPE[entry.entry_type]) {
      throw new Error(
        `author_type 与 entry_type 不匹配：${entry.entry_id}；导入已停止，未进行来源重分配。`,
      );
    }
    if (!/^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$/.test(entry.created_at)) {
      throw new Error(`created_at 必须包含明确时区：${entry.entry_id}`);
    }
    if (!CONFIDENCE_VALUES.has(entry.confidence)) {
      throw new Error(`confidence 无效：${entry.entry_id}`);
    }
    if (!VERIFICATION_VALUES.has(entry.verification)) {
      throw new Error(`verification 无效：${entry.entry_id}`);
    }
    if (entry.entry_type === "llm_answer") {
      assertString(entry.question_entry_id, `entry.question_entry_id (${entry.entry_id})`);
      if (Object.prototype.hasOwnProperty.call(entry, "model_label")) {
        assertString(entry.model_label, `entry.model_label (${entry.entry_id})`);
      }
    } else if (
      Object.prototype.hasOwnProperty.call(entry, "question_entry_id") ||
      Object.prototype.hasOwnProperty.call(entry, "model_label")
    ) {
      throw new Error(`只有 llm_answer 可以包含问题链接或模型标签：${entry.entry_id}`);
    }
  }

  function validateSessionPayload(payload) {
    assertObject(payload, "session payload");
    assertAllowedKeys(
      payload,
      new Set([
        "format_version",
        "source_label",
        "session_id",
        "session_state",
        "entries",
        "preferences",
        "exported_at",
        "saved_at",
      ]),
      "session payload",
    );
    if (payload.format_version !== FORMAT_VERSION) {
      throw new Error(`不支持的会话格式：${String(payload.format_version)}`);
    }
    assertString(payload.source_label, "source_label");
    assertString(payload.session_id, "session_id");
    if (payload.source_label !== BOOTSTRAP.source_label || payload.session_id !== BOOTSTRAP.session_id) {
      throw new Error("会话来源与当前生成页面不一致；现有会话未被替换。");
    }
    if (payload.session_state !== "active") {
      throw new Error("RW-01 只能导入 active 阅读会话。");
    }
    if (!Array.isArray(payload.entries)) throw new Error("entries 必须是数组。");
    validatePreferences(payload.preferences);
    const entryIds = new Set();
    payload.entries.forEach((entry) => validateEntry(entry, entryIds));
    const entryById = new Map(payload.entries.map((entry) => [entry.entry_id, entry]));
    payload.entries.forEach((entry) => {
      if (entry.entry_type !== "llm_answer") return;
      const question = entryById.get(entry.question_entry_id);
      if (!question) {
        throw new Error(`LLM 回答链接的问题不存在：${entry.entry_id}`);
      }
      if (question.entry_type !== "human_question") {
        throw new Error(`LLM 回答必须链接 human_question：${entry.entry_id}`);
      }
      ReadingWorkspaceModel.validateSelectionFields(entry, question);
    });
    if (Object.prototype.hasOwnProperty.call(payload, "exported_at")) {
      assertString(payload.exported_at, "exported_at");
    }
    if (Object.prototype.hasOwnProperty.call(payload, "saved_at")) {
      assertString(payload.saved_at, "saved_at");
    }
    return payload;
  }

  function applyPayload(payload, message) {
    state = {
      entries: clone(payload.entries),
      preferences: clone(payload.preferences),
    };
    renderAll();
    setSaveState("saved", message);
  }

  function persistState() {
    setSaveState("unsaved", "未保存");
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sessionPayload("saved_at")));
      setSaveState("saved", "本地已保存");
      return true;
    } catch (error) {
      setSaveState("error", "本地保存失败");
      setMessage(`本地恢复数据保存失败：${error.message}`, "error");
      return false;
    }
  }

  function mutate(mutator, message = "会话已更新。") {
    setSaveState("unsaved", "未保存");
    mutator();
    renderAll();
    if (persistState()) setMessage(message, "success");
  }

  function offerRecovery() {
    try {
      const serialized = localStorage.getItem(STORAGE_KEY);
      if (!serialized) return;
      const parsed = JSON.parse(serialized);
      validateSessionPayload(parsed);
      recoveryDraft = parsed;
      elements.recoverySummary.textContent = `${parsed.entries.length} 个条目 · ${parsed.saved_at || "保存时间未知"}`;
      elements.recoveryBanner.hidden = false;
      setSaveState("recovery", "有草稿可恢复");
    } catch (error) {
      setSaveState("error", "恢复数据不可用");
      setMessage(`发现本地恢复数据，但无法安全读取：${error.message}`, "error");
    }
  }

  function clearRecoveryData(label) {
    try {
      localStorage.removeItem(STORAGE_KEY);
      recoveryDraft = null;
      elements.recoveryBanner.hidden = true;
      if (state.entries.length) {
        setSaveState("unsaved", "恢复数据已清除");
      } else {
        setSaveState("idle", "尚无本地草稿");
      }
      setMessage(label, "success");
    } catch (error) {
      setSaveState("error", "清除失败");
      setMessage(`无法清除本地恢复数据：${error.message}`, "error");
    }
  }

  function nextEntryId() {
    const used = new Set(state.entries.map((entry) => entry.entry_id));
    let sequence = 1;
    while (used.has(`rw-entry-${String(sequence).padStart(4, "0")}`)) sequence += 1;
    return `rw-entry-${String(sequence).padStart(4, "0")}`;
  }

  function currentQuestionEntries() {
    return state.entries.filter((entry) => entry.entry_type === "human_question");
  }

  function updateHighlights() {
    const preferences = state.preferences;
    const mutedConcepts = new Set(preferences.muted_concepts);
    const mutedTerms = new Set(preferences.muted_terms);
    const seenParagraph = new Set();
    const seenSection = new Set();
    document.querySelectorAll(".concept-hit").forEach((hit) => {
      const concept = hit.dataset.concept;
      const termKey = hit.dataset.termKey;
      const paragraphKey = `${hit.dataset.blockId}\u0000${concept}`;
      const sectionKey = `${hit.dataset.sectionId}\u0000${concept}`;
      let suppressed = !preferences.highlights_enabled;
      if (mutedConcepts.has(concept) || mutedTerms.has(termKey)) suppressed = true;
      if (!suppressed && preferences.density === "paragraph") {
        if (seenParagraph.has(paragraphKey)) suppressed = true;
        seenParagraph.add(paragraphKey);
      }
      if (!suppressed && preferences.density === "section") {
        if (seenSection.has(sectionKey)) suppressed = true;
        seenSection.add(sectionKey);
      }
      hit.classList.toggle("is-suppressed", suppressed);
      hit.tabIndex = suppressed ? -1 : 0;
    });
    renderMutedSummary();
  }

  function renderMutedSummary() {
    const concepts = state.preferences.muted_concepts;
    const terms = state.preferences.muted_terms;
    elements.mutedSummary.replaceChildren();
    if (!concepts.length && !terms.length) {
      elements.mutedSummary.hidden = true;
      return;
    }
    elements.mutedSummary.hidden = false;
    elements.mutedSummary.append(createElement("strong", "", "本会话静音项"));
    const list = createElement("div", "muted-list");
    concepts.forEach((concept) => {
      const button = createElement("button", "muted-chip", `概念：${concept} ×`);
      button.type = "button";
      button.addEventListener("click", () => {
        mutate(() => {
          state.preferences.muted_concepts = state.preferences.muted_concepts.filter((item) => item !== concept);
        }, "已恢复该概念的高亮。");
      });
      list.append(button);
    });
    terms.forEach((term) => {
      const button = createElement("button", "muted-chip", `词：${term} ×`);
      button.type = "button";
      button.addEventListener("click", () => {
        mutate(() => {
          state.preferences.muted_terms = state.preferences.muted_terms.filter((item) => item !== term);
        }, "已恢复该匹配词的高亮。");
      });
      list.append(button);
    });
    elements.mutedSummary.append(list);
  }

  function addField(container, label, value, className = "") {
    const wrapper = createElement("div", `entry-field ${className}`.trim());
    wrapper.append(createElement("span", "entry-field-label", label));
    wrapper.append(createElement("div", "entry-field-value", value));
    container.append(wrapper);
  }

  function selectControl(entry, field, values) {
    const label = createElement("label", "metadata-control");
    label.append(createElement("span", "", field === "confidence" ? "信心" : "核验"));
    const select = document.createElement("select");
    select.dataset.entryId = entry.entry_id;
    select.dataset.field = field;
    values.forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      option.selected = entry[field] === value;
      select.append(option);
    });
    select.addEventListener("change", () => {
      mutate(() => {
        const target = state.entries.find((item) => item.entry_id === entry.entry_id);
        target[field] = select.value;
      }, `${field} 已更新。`);
    });
    label.append(select);
    return label;
  }

  function renderEntryCard(entry, entryById) {
    const card = createElement("article", "entry-card");
    card.dataset.entryId = entry.entry_id;
    const header = createElement("header", "entry-card-header");
    const identity = createElement("div");
    identity.append(createElement("p", "entry-id", entry.entry_id));
    identity.append(createElement("h3", "", ENTRY_TYPE_LABELS[entry.entry_type]));
    header.append(identity);
    const badges = createElement("div", "entry-badges");
    badges.append(createElement("span", "origin-badge", entry.author_type));
    if (ReadingWorkspaceModel.selectedTextOrigin(entry) === SELECTED_TEXT_ORIGINS.translation) {
      badges.append(
        createElement("span", "translation-origin-badge", TRANSLATION_PROVENANCE),
      );
    }
    header.append(badges);
    card.append(header);

    addField(card, "来源定位", entry.source_locator);
    if (entry.selected_text) addField(card, "选中文本", entry.selected_text, "selected-context");
    addField(card, "内容", entry.content, "entry-content");
    if (entry.entry_type === "llm_answer") {
      const question = entryById.get(entry.question_entry_id);
      const questionLabel = question
        ? `${question.entry_id} · ${question.content}`
        : `${entry.question_entry_id} · 链接无效`;
      addField(card, "对应问题", questionLabel, "linked-question");
      if (entry.model_label) addField(card, "模型标签", entry.model_label);
    }
    const timestamp = createElement("time", "entry-time", entry.created_at);
    timestamp.dateTime = entry.created_at;
    card.append(timestamp);

    const controls = createElement("div", "entry-metadata-controls");
    controls.append(selectControl(entry, "confidence", [...CONFIDENCE_VALUES]));
    controls.append(selectControl(entry, "verification", [...VERIFICATION_VALUES]));
    card.append(controls);

    const actions = createElement("div", "entry-actions");
    if (entry.entry_type === "human_question") {
      const packetButton = createElement("button", "", "问题包");
      packetButton.type = "button";
      packetButton.addEventListener("click", () => openQuestionPacket(entry.entry_id));
      actions.append(packetButton);
    }
    if (entry.entry_type !== "llm_answer") {
      const editButton = createElement("button", "", "编辑");
      editButton.type = "button";
      editButton.addEventListener("click", () => openEntryDialog(entry.entry_type, entry));
      actions.append(editButton);
    }
    const deleteButton = createElement("button", "danger", "删除");
    deleteButton.type = "button";
    deleteButton.addEventListener("click", () => deleteEntry(entry.entry_id));
    actions.append(deleteButton);
    card.append(actions);
    return card;
  }

  function updateSessionTabs() {
    elements.sessionTabs.forEach((button) => {
      const tabName = button.dataset.sessionTab;
      const selected = tabName === activeSessionTab;
      const count = ReadingWorkspaceModel.entriesForTab(state.entries, tabName).length;
      button.setAttribute("aria-selected", String(selected));
      button.tabIndex = selected ? 0 : -1;
      button.querySelector("[data-tab-count]").textContent = String(count);
      if (selected) elements.sessionList.setAttribute("aria-labelledby", button.id);
    });
  }

  function appendEmptyState(message) {
    elements.sessionList.append(createElement("p", "empty-state", message));
  }

  function renderQuestionAnswerGroups(entryById) {
    const groups = ReadingWorkspaceModel.groupQuestionAnswers(state.entries);
    if (!groups.length) {
      appendEmptyState("尚无人类问题。");
      return;
    }
    groups.forEach(({ question, answers }) => {
      const group = createElement("section", "qa-group");
      group.dataset.questionEntryId = question.entry_id;
      group.dataset.selectedTextOrigin = ReadingWorkspaceModel.selectedTextOrigin(question);
      if (group.dataset.selectedTextOrigin === SELECTED_TEXT_ORIGINS.translation) {
        group.append(
          createElement("p", "qa-origin-boundary", TRANSLATION_PROVENANCE),
        );
      }
      const questionColumn = createElement("div", "qa-question-column");
      questionColumn.append(createElement("p", "qa-column-label", "问题"));
      questionColumn.append(renderEntryCard(question, entryById));

      const answerColumn = createElement("div", "qa-answer-column");
      answerColumn.append(
        createElement("p", "qa-column-label", `回答 (${answers.length})`),
      );
      if (!answers.length) {
        answerColumn.append(createElement("p", "unanswered-state", "尚无回答"));
      } else {
        answers.forEach((answer) => {
          answerColumn.append(renderEntryCard(answer, entryById));
        });
      }
      group.append(questionColumn, answerColumn);
      elements.sessionList.append(group);
    });
  }

  function renderEntries() {
    elements.entryCount.textContent = String(state.entries.length);
    elements.sessionList.replaceChildren();
    updateSessionTabs();
    if (!state.entries.length) {
      appendEmptyState("选择正文后创建摘录、笔记或问题。");
      return;
    }
    const entryById = new Map(state.entries.map((entry) => [entry.entry_id, entry]));
    if (activeSessionTab === "qa") {
      renderQuestionAnswerGroups(entryById);
      return;
    }
    const entries = ReadingWorkspaceModel.entriesForTab(state.entries, activeSessionTab);
    if (!entries.length) {
      appendEmptyState(activeSessionTab === "excerpts" ? "尚无来源摘录。" : "尚无个人笔记。");
      return;
    }
    entries.forEach((entry) => {
      elements.sessionList.append(renderEntryCard(entry, entryById));
    });
  }

  function sourceBlockOrigin(block) {
    if (Object.values(SELECTED_TEXT_ORIGINS).includes(block.dataset.sourceOrigin)) {
      return block.dataset.sourceOrigin;
    }
    return block.dataset.blockId && block.dataset.blockId.startsWith("translation-")
      ? SELECTED_TEXT_ORIGINS.translation
      : SELECTED_TEXT_ORIGINS.authoritative;
  }

  function visibleBlockText(block) {
    const walker = document.createTreeWalker(block, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const parent = node.parentElement;
        if (parent && parent.closest(".hover-card, [role='tooltip'], .annotation-badge")) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    const fragments = [];
    while (walker.nextNode()) fragments.push(walker.currentNode.nodeValue || "");
    return fragments.join(" ");
  }

  function updateAnnotations() {
    const blocks = [...document.querySelectorAll("[data-source-block][data-block-id]")];
    blocks.forEach((block) => {
      block.classList.remove("is-annotated");
      delete block.dataset.annotationCount;
      block.querySelectorAll(":scope > .annotation-badge").forEach((badge) => badge.remove());
    });
    const descriptors = blocks.map((block, index) => ({
      block_key: String(index),
      block_id: block.dataset.blockId,
      source_origin: sourceBlockOrigin(block),
      source_locator: block.dataset.locator || "not_available",
      visible_text: visibleBlockText(block),
    }));
    const result = ReadingWorkspaceModel.resolveBlockAnnotations(
      state.entries,
      descriptors,
    );
    Object.entries(result.blockCounts).forEach(([blockKey, count]) => {
      const block = blocks[Number(blockKey)];
      if (!block) return;
      block.classList.add("is-annotated");
      block.dataset.annotationCount = String(count);
      const badge = createElement("span", "annotation-badge", `批注 ${count}`);
      badge.setAttribute("aria-label", `${count} 条阅读批注`);
      badge.title = `${count} 条阅读批注`;
      block.append(badge);
    });
    if (elements.annotationLocationStatus) {
      elements.annotationLocationStatus.hidden = result.unlocatedCount === 0;
      elements.annotationLocationStatus.textContent = `未定位批注：${result.unlocatedCount}`;
    }
  }

  function renderAll() {
    elements.density.value = state.preferences.density;
    elements.highlightToggle.checked = state.preferences.highlights_enabled;
    applyReferenceMode(elements.referenceMode ? elements.referenceMode.value : "english");
    renderEntries();
    updateHighlights();
    updateAnnotations();
  }

  function handleConceptAction(event) {
    const action = event.target.closest("button[data-action]");
    if (!action) return;
    const hit = action.closest(".concept-hit");
    if (!hit) return;
    event.preventDefault();
    event.stopPropagation();
    if (action.dataset.action === "mute-concept") {
      mutate(() => {
        if (!state.preferences.muted_concepts.includes(hit.dataset.concept)) {
          state.preferences.muted_concepts.push(hit.dataset.concept);
        }
      }, `已在本会话静音概念：${hit.dataset.concept}`);
    } else if (action.dataset.action === "mute-term") {
      mutate(() => {
        if (!state.preferences.muted_terms.includes(hit.dataset.termKey)) {
          state.preferences.muted_terms.push(hit.dataset.termKey);
        }
      }, `已在本会话静音匹配词：${hit.dataset.termLabel}`);
    }
  }

  function clearCurrentSelection() {
    currentSelection = null;
    elements.selectionTools.hidden = true;
    elements.selectionPreview.textContent = "";
    if (elements.selectionOriginNote) elements.selectionOriginNote.hidden = true;
    const excerptButton = elements.selectionSourceExcerpt || document.querySelector(
      '[data-create-entry="source_excerpt"]',
    );
    if (excerptButton) {
      excerptButton.hidden = false;
      excerptButton.disabled = false;
      excerptButton.removeAttribute("aria-disabled");
    }
    delete elements.selectionTools.dataset.sourceOrigin;
  }

  function selectionBlockForNode(node) {
    if (!node) return null;
    const element = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
    return element ? element.closest("[data-source-block][data-block-id]") : null;
  }

  function selectedVisibleText(range) {
    const fragment = range.cloneContents();
    fragment.querySelectorAll(".hover-card, [role='tooltip'], .annotation-badge").forEach(
      (node) => node.remove(),
    );
    return fragment.textContent || "";
  }

  function showSelectionTools(origin, selectedText) {
    const isTranslation = origin === SELECTED_TEXT_ORIGINS.translation;
    elements.selectionPreview.textContent = selectedText.replace(/\s+/g, " ").slice(0, 180);
    elements.selectionTools.dataset.sourceOrigin = origin;
    if (elements.selectionOriginNote) {
      elements.selectionOriginNote.hidden = !isTranslation;
      elements.selectionOriginNote.textContent = isTranslation ? TRANSLATION_PROVENANCE : "";
    }
    const excerptButton = elements.selectionSourceExcerpt || document.querySelector(
      '[data-create-entry="source_excerpt"]',
    );
    if (excerptButton) {
      excerptButton.hidden = isTranslation;
      excerptButton.disabled = isTranslation;
      if (isTranslation) excerptButton.setAttribute("aria-disabled", "true");
      else excerptButton.removeAttribute("aria-disabled");
    }
    elements.selectionTools.hidden = false;
  }

  function captureSelection() {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed || !selection.rangeCount) {
      clearCurrentSelection();
      return;
    }
    const range = selection.getRangeAt(0);
    const startBlock = selectionBlockForNode(range.startContainer);
    const endBlock = selectionBlockForNode(range.endContainer);
    const selectionRoot = selectionRoots.find(
      (root) => startBlock && endBlock && root.contains(startBlock) && root.contains(endBlock),
    );
    if (!selectionRoot || startBlock !== endBlock) {
      clearCurrentSelection();
      if (startBlock || endBlock) {
        setMessage("一次选区必须位于同一个正文或图表块内。", "error");
      }
      return;
    }
    const selectedText = selectedVisibleText(range);
    if (!selectedText.trim()) {
      clearCurrentSelection();
      return;
    }
    const origin = sourceBlockOrigin(startBlock);
    if (!Object.values(SELECTED_TEXT_ORIGINS).includes(origin)) {
      clearCurrentSelection();
      setMessage("无法确定选区来源；未创建条目。", "error");
      return;
    }
    currentSelection = {
      selected_text: selectedText,
      source_locator: startBlock.dataset.locator || "not_available",
      selected_text_origin: origin,
      selected_block_id: startBlock.dataset.blockId,
    };
    showSelectionTools(origin, selectedText);
  }

  function openEntryDialog(entryType, entry = null) {
    if (!entry && !currentSelection) {
      setMessage("请先在阅读正文中选择文本。", "error");
      return;
    }
    if (
      !entry &&
      entryType === "source_excerpt" &&
      currentSelection.selected_text_origin === SELECTED_TEXT_ORIGINS.translation
    ) {
      setMessage("中文参考译文仅可创建个人笔记或问题，不能保存来源摘录。", "error");
      return;
    }
    editingEntryId = entry ? entry.entry_id : null;
    elements.entryForm.dataset.entryType = entryType;
    elements.entryDialogType.textContent = ENTRY_TYPE_LABELS[entryType];
    elements.entryDialogTitle.textContent = entry ? "编辑条目" : "创建条目";
    const selectionOrigin = entry
      ? ReadingWorkspaceModel.selectedTextOrigin(entry)
      : currentSelection.selected_text_origin;
    elements.entryOrigin.textContent = selectionOrigin === SELECTED_TEXT_ORIGINS.translation
      ? `${AUTHOR_BY_ENTRY_TYPE[entryType]} · ${TRANSLATION_PROVENANCE}`
      : `${AUTHOR_BY_ENTRY_TYPE[entryType]} · 英文权威来源`;
    elements.entryLocator.value = entry ? entry.source_locator : currentSelection.source_locator;
    elements.entrySelectedText.value = entry ? entry.selected_text : currentSelection.selected_text;
    elements.entryContent.readOnly = entryType === "source_excerpt";
    if (entry) {
      elements.entryContent.value = entry.content;
    } else if (entryType === "source_excerpt") {
      elements.entryContent.value = currentSelection.selected_text;
    } else {
      elements.entryContent.value = "";
    }
    elements.entryDialog.showModal();
  }

  function saveEntry(event) {
    event.preventDefault();
    const entryType = elements.entryForm.dataset.entryType;
    const locator = elements.entryLocator.value.trim() || "not_available";
    const content = elements.entryContent.value;
    if (!content.trim()) {
      setMessage("条目内容不能为空。", "error");
      return;
    }
    if (editingEntryId) {
      mutate(() => {
        const entry = state.entries.find((item) => item.entry_id === editingEntryId);
        entry.source_locator = locator;
        if (entry.entry_type === "human_note" || entry.entry_type === "human_question") {
          entry.content = content;
        }
      }, "条目已显式更新并保存到本地恢复数据。");
    } else {
      if (!currentSelection) {
        setMessage("选区已失效，请重新选择文本。", "error");
        return;
      }
      const defaults = ENTRY_DEFAULTS[entryType];
      const entry = {
        entry_id: nextEntryId(),
        entry_type: entryType,
        created_at: new Date().toISOString(),
        author_type: AUTHOR_BY_ENTRY_TYPE[entryType],
        source_locator: locator,
        selected_text: currentSelection.selected_text,
        content,
        confidence: defaults.confidence,
        verification: defaults.verification,
        selected_text_origin: currentSelection.selected_text_origin,
        selected_block_id: currentSelection.selected_block_id,
      };
      try {
        ReadingWorkspaceModel.validateSelectionFields(entry);
      } catch (error) {
        setMessage(error.message, "error");
        return;
      }
      mutate(() => state.entries.push(entry), "条目已创建并保存到本地恢复数据。");
    }
    elements.entryDialog.close();
    editingEntryId = null;
    window.getSelection().removeAllRanges();
    clearCurrentSelection();
  }

  function deleteEntry(entryId) {
    const linkedAnswers = state.entries.filter(
      (entry) => entry.entry_type === "llm_answer" && entry.question_entry_id === entryId,
    );
    if (linkedAnswers.length) {
      setMessage("该问题仍有链接的 LLM 回答；请先显式删除回答。", "error");
      return;
    }
    if (!window.confirm(`确认删除条目 ${entryId}？此操作会更新本地恢复草稿。`)) return;
    mutate(() => {
      state.entries = state.entries.filter((entry) => entry.entry_id !== entryId);
    }, `已删除 ${entryId}。`);
  }

  function openAnswerDialog() {
    const questions = currentQuestionEntries();
    if (!questions.length) {
      setMessage("请先创建至少一个人类问题。", "error");
      return;
    }
    elements.answerQuestion.replaceChildren();
    questions.forEach((question) => {
      const option = document.createElement("option");
      option.value = question.entry_id;
      const originLabel = ReadingWorkspaceModel.selectedTextOrigin(question) === SELECTED_TEXT_ORIGINS.translation
        ? " · 中文参考"
        : "";
      option.textContent = `${question.entry_id}${originLabel} · ${question.content}`;
      elements.answerQuestion.append(option);
    });
    elements.answerModelLabel.value = "";
    elements.answerContent.value = "";
    elements.answerDialog.showModal();
  }

  function saveAnswer(event) {
    event.preventDefault();
    const question = state.entries.find(
      (entry) => entry.entry_id === elements.answerQuestion.value && entry.entry_type === "human_question",
    );
    if (!question) {
      setMessage("选择的问题不存在，回答未保存。", "error");
      return;
    }
    const content = elements.answerContent.value;
    if (!content.trim()) {
      setMessage("LLM 回答不能为空。", "error");
      return;
    }
    const defaults = ENTRY_DEFAULTS.llm_answer;
    const answer = {
      entry_id: nextEntryId(),
      entry_type: "llm_answer",
      created_at: new Date().toISOString(),
      author_type: AUTHOR_BY_ENTRY_TYPE.llm_answer,
      source_locator: question.source_locator,
      selected_text: question.selected_text,
      content,
      confidence: defaults.confidence,
      verification: defaults.verification,
      question_entry_id: question.entry_id,
      selected_text_origin: ReadingWorkspaceModel.selectedTextOrigin(question),
    };
    if (Object.prototype.hasOwnProperty.call(question, "selected_block_id")) {
      answer.selected_block_id = question.selected_block_id;
    }
    const modelLabel = elements.answerModelLabel.value.trim();
    if (modelLabel) answer.model_label = modelLabel;
    try {
      ReadingWorkspaceModel.validateSelectionFields(answer, question);
    } catch (error) {
      setMessage(error.message, "error");
      return;
    }
    mutate(() => state.entries.push(answer), "LLM 回答已粘贴、链接并保存到本地恢复数据。");
    elements.answerDialog.close();
  }

  function questionPacket(question) {
    return [
      "# 外部 LLM 问题包",
      "",
      `来源：${BOOTSTRAP.source_label}`,
      `来源定位：${question.source_locator}`,
      `选区来源：${ReadingWorkspaceModel.selectedTextOrigin(question) === SELECTED_TEXT_ORIGINS.translation ? TRANSLATION_PROVENANCE : "英文权威来源"}`,
      "",
      "## 选中文本",
      "",
      question.selected_text || "not_available",
      "",
      "## 人类问题",
      "",
      question.content,
      "",
      "请仅返回辅助回答；此工作区不会自动发送或导入回答。",
      "",
    ].join("\n");
  }

  function openQuestionPacket(entryId) {
    const question = state.entries.find(
      (entry) => entry.entry_id === entryId && entry.entry_type === "human_question",
    );
    if (!question) return;
    elements.packetContent.value = questionPacket(question);
    elements.packetDialog.showModal();
  }

  async function copyQuestionPacket() {
    const packet = elements.packetContent.value;
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error("clipboard unavailable");
      await navigator.clipboard.writeText(packet);
      setMessage("问题包已复制；请由人手动粘贴到外部 LLM。", "success");
    } catch (_error) {
      elements.packetContent.focus();
      elements.packetContent.select();
      const copied = document.execCommand("copy");
      setMessage(
        copied ? "问题包已复制；请由人手动粘贴到外部 LLM。" : "自动复制不可用；问题包已选中，请手动复制。",
        copied ? "success" : "error",
      );
    }
  }

  function buildSessionMarkdown() {
    return ReadingWorkspaceModel.buildSessionMarkdownEnvelope(
      sessionPayload("exported_at"),
    );
  }

  function exportFilename() {
    const basename = BOOTSTRAP.source_label.split("/").pop().replace(/\.md$/i, "");
    const safe = basename.replace(/[\\/:*?\"<>|]/g, "-").trim() || "reading-session";
    return `${safe}.reading-session.md`;
  }

  function downloadSession() {
    const markdown = buildSessionMarkdown();
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    const objectUrl = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = objectUrl;
    anchor.download = exportFilename();
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    window.setTimeout(() => URL.revokeObjectURL(objectUrl), 0);
    setMessage("会话 Markdown 已导出；它是可移植、可 Git 审阅的会话 artifact。", "success");
  }

  function parseSessionMarkdown(markdown) {
    return validateSessionPayload(
      ReadingWorkspaceModel.parseSessionMarkdownEnvelope(markdown),
    );
  }

  function importSessionMarkdown(markdown, requireConfirmation = true) {
    const validated = parseSessionMarkdown(markdown);
    const hasWork = state.entries.length > 0 || recoveryDraft !== null;
    if (
      requireConfirmation &&
      hasWork &&
      !window.confirm("导入会替换当前非空会话或可恢复草稿。确认继续？")
    ) {
      setMessage("已取消导入；当前会话保持不变。", "info");
      return false;
    }
    state = {
      entries: clone(validated.entries),
      preferences: clone(validated.preferences),
    };
    recoveryDraft = null;
    elements.recoveryBanner.hidden = true;
    renderAll();
    const persisted = persistState();
    setMessage(
      persisted
        ? "会话导入成功；条目顺序、ID 和问题链接已保留。"
        : "会话已导入到当前页面，但本地恢复数据保存失败；请立即导出 Markdown。",
      persisted ? "success" : "error",
    );
    return true;
  }

  function handleImportFile() {
    const file = elements.importSession.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onerror = () => setMessage("无法读取所选会话文件；当前会话保持不变。", "error");
    reader.onload = () => {
      try {
        importSessionMarkdown(String(reader.result));
      } catch (error) {
        setMessage(`导入失败：${error.message} 当前会话保持不变。`, "error");
      } finally {
        elements.importSession.value = "";
      }
    };
    reader.readAsText(file, "UTF-8");
  }

  function bindPresentationResizer(resizer) {
    const handle = resizer.dataset.resizer;
    let drag = null;

    function finishDrag(event) {
      if (!drag || event.pointerId !== drag.pointerId) return;
      if (resizer.hasPointerCapture(event.pointerId)) {
        resizer.releasePointerCapture(event.pointerId);
      }
      drag = null;
      resizer.classList.remove("is-dragging");
      document.body.classList.remove("is-resizing-layout");
      persistPresentationLayout("阅读栏宽已保存。若需默认值，可双击分隔条或使用重置布局。");
    }

    resizer.addEventListener("pointerdown", (event) => {
      if (event.button !== 0 || resizer.hidden) return;
      event.preventDefault();
      drag = {
        pointerId: event.pointerId,
        startX: event.clientX,
        initialLayout: clone(presentationLayout),
        metrics: presentationMetrics(),
      };
      resizer.setPointerCapture(event.pointerId);
      resizer.classList.add("is-dragging");
      document.body.classList.add("is-resizing-layout");
    });
    resizer.addEventListener("pointermove", (event) => {
      if (!drag || event.pointerId !== drag.pointerId) return;
      const next = ReadingWorkspaceModel.resizePresentationLayout(
        drag.initialLayout,
        handle,
        event.clientX - drag.startX,
        drag.metrics,
      );
      applyPresentationLayout(next);
    });
    resizer.addEventListener("pointerup", finishDrag);
    resizer.addEventListener("pointercancel", finishDrag);
    resizer.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight"].includes(event.key)) return;
      event.preventDefault();
      const step = event.shiftKey ? 48 : 16;
      const delta = event.key === "ArrowLeft" ? -step : step;
      const next = ReadingWorkspaceModel.resizePresentationLayout(
        presentationLayout,
        handle,
        delta,
        presentationMetrics(),
      );
      setPresentationLayout(next, "阅读栏宽已通过键盘调整并保存。");
    });
    resizer.addEventListener("dblclick", (event) => {
      event.preventDefault();
      resetPresentationLayout();
    });
  }

  elements.density.addEventListener("change", () => {
    mutate(() => {
      state.preferences.density = elements.density.value;
    }, "高亮密度已更新。");
  });
  elements.highlightToggle.addEventListener("change", () => {
    mutate(() => {
      state.preferences.highlights_enabled = elements.highlightToggle.checked;
    }, "概念高亮显示状态已更新。");
  });
  elements.sessionPanelWidth.addEventListener("change", applySessionPanelPreset);
  if (elements.referenceMode) {
    elements.referenceMode.addEventListener("change", () => {
      applyReferenceMode(elements.referenceMode.value);
      clearCurrentSelection();
      applyPresentationLayout(presentationLayout);
    });
  }
  if (elements.resetLayout) elements.resetLayout.addEventListener("click", resetPresentationLayout);
  resizers.forEach(bindPresentationResizer);
  elements.restoreMuted.addEventListener("click", () => {
    mutate(() => {
      state.preferences.muted_concepts = [];
      state.preferences.muted_terms = [];
    }, "已恢复所有静音概念和匹配词。");
  });
  selectionRoots.forEach((surface) => {
    surface.addEventListener("mouseup", () => window.setTimeout(captureSelection, 0));
    surface.addEventListener("keyup", captureSelection);
    surface.addEventListener("click", handleConceptAction);
  });
  document.querySelectorAll("[data-create-entry]").forEach((button) => {
    button.addEventListener("click", () => openEntryDialog(button.dataset.createEntry));
  });
  document.querySelectorAll("[data-close-dialog]").forEach((button) => {
    button.addEventListener("click", () => document.getElementById(button.dataset.closeDialog).close());
  });
  elements.sessionTabs.forEach((button, index, tabs) => {
    button.addEventListener("click", () => {
      activeSessionTab = button.dataset.sessionTab;
      renderEntries();
    });
    button.addEventListener("keydown", (event) => {
      let nextIndex = null;
      if (event.key === "ArrowLeft") nextIndex = (index - 1 + tabs.length) % tabs.length;
      if (event.key === "ArrowRight") nextIndex = (index + 1) % tabs.length;
      if (event.key === "Home") nextIndex = 0;
      if (event.key === "End") nextIndex = tabs.length - 1;
      if (nextIndex === null) return;
      event.preventDefault();
      tabs[nextIndex].focus();
      tabs[nextIndex].click();
    });
  });
  elements.entryForm.addEventListener("submit", saveEntry);
  elements.addAnswer.addEventListener("click", openAnswerDialog);
  elements.answerForm.addEventListener("submit", saveAnswer);
  elements.copyPacket.addEventListener("click", copyQuestionPacket);
  elements.exportSession.addEventListener("click", downloadSession);
  elements.importSession.addEventListener("change", handleImportFile);
  elements.recoverDraft.addEventListener("click", () => {
    if (!recoveryDraft) return;
    applyPayload(recoveryDraft, "本地草稿已恢复");
    recoveryDraft = null;
    elements.recoveryBanner.hidden = true;
    setMessage("已恢复最新本地会话草稿。", "success");
  });
  elements.discardDraft.addEventListener("click", () => {
    if (!window.confirm("确认清除可恢复的本地草稿？此操作不会删除已导出的 Markdown。")) return;
    clearRecoveryData("可恢复草稿已由人显式清除。");
  });
  elements.clearRecovery.addEventListener("click", () => {
    if (!window.confirm("确认清除本页面对应来源的本地恢复数据？")) return;
    clearRecoveryData("本地恢复数据已由人显式清除。");
  });

  window.ReadingWorkspace = Object.freeze({
    formatVersion: FORMAT_VERSION,
    buildSessionMarkdown,
    importSessionMarkdown,
    snapshot: () => clone(sessionPayload()),
  });

  let resizeFrame = null;
  window.addEventListener("resize", () => {
    if (resizeFrame !== null) window.cancelAnimationFrame(resizeFrame);
    resizeFrame = window.requestAnimationFrame(() => {
      resizeFrame = null;
      applyPresentationLayout(presentationLayout);
    });
  });

  restorePresentationLayout();
  renderAll();
  offerRecovery();
})();
}
