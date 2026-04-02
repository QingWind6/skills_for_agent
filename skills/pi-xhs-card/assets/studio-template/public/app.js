const TEMPLATES = [
  {
    id: "editorial-tech",
    label: "编辑部科技风",
    short: "Editorial Tech",
    description: "适合 AI、开源、趋势观察，强调大标题和编辑感。"
  },
  {
    id: "knowledge-clean",
    label: "极简知识卡",
    short: "Knowledge Clean",
    description: "适合清单、教程、工具推荐，信息层级清晰。"
  },
  {
    id: "study-notes",
    label: "学习笔记风",
    short: "Study Notes",
    description: "适合方法论、总结、读书笔记，氛围更轻松。"
  }
];

const TYPE_LABELS = {
  cover: "封面",
  ranking: "榜单",
  insight: "洞察",
  closing: "收尾"
};

const state = {
  deck: null,
  selectedIndex: 0,
  dirty: false,
  exportRuns: [],
  layoutIssues: [],
  mode: new URLSearchParams(window.location.search).get("mode") || "editor"
};

const els = {
  app: document.getElementById("app"),
  deckTitle: document.getElementById("deckTitle"),
  deckSubtitle: document.getElementById("deckSubtitle"),
  templateList: document.getElementById("templateList"),
  cardList: document.getElementById("cardList"),
  issueList: document.getElementById("issueList"),
  previewRoot: document.getElementById("previewRoot"),
  editorForm: document.getElementById("editorForm"),
  statusText: document.getElementById("statusText"),
  dirtyBadge: document.getElementById("dirtyBadge"),
  saveButton: document.getElementById("saveButton"),
  reloadButton: document.getElementById("reloadButton"),
  exportButton: document.getElementById("exportButton"),
  moveUpButton: document.getElementById("moveUpButton"),
  moveDownButton: document.getElementById("moveDownButton"),
  exportList: document.getElementById("exportList")
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function clone(value) {
  return structuredClone(value);
}

function currentCard() {
  return state.deck.cards[state.selectedIndex];
}

function currentTemplateId() {
  return state.deck?.meta?.templateId || TEMPLATES[0].id;
}

function currentTemplate() {
  return TEMPLATES.find((template) => template.id === currentTemplateId()) || TEMPLATES[0];
}

function typeLabel(type) {
  return TYPE_LABELS[type] || type;
}

function setStatus(text, isError = false) {
  els.statusText.textContent = text;
  els.statusText.style.color = isError ? "var(--danger)" : "var(--muted)";
}

function setDirty(value) {
  state.dirty = value;
  els.dirtyBadge.classList.toggle("is-hidden", !value);
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || payload.message || "Request failed");
  }
  return payload;
}

async function loadDeck() {
  const deck = await fetchJson("/api/deck");
  state.deck = deck;
  if (!state.deck.meta.templateId) {
    state.deck.meta.templateId = TEMPLATES[0].id;
  }
  setDirty(false);
}

async function loadExports() {
  const data = await fetchJson("/api/exports");
  state.exportRuns = data.runs;
}

function cardSummary(card) {
  switch (card.type) {
    case "cover":
      return card.subtitle || "封面";
    case "ranking":
      return `${card.rows.length} 条榜单`;
    case "insight":
      return `${card.blocks.length} 条趋势结论`;
    case "closing":
      return `${card.groups.length} 条关注方向`;
    default:
      return card.type;
  }
}

function updateHeader() {
  els.deckTitle.textContent = state.deck.meta.title || "未命名卡片集";
  const template = currentTemplate();
  els.deckSubtitle.textContent = `${state.deck.meta.subtitle || ""} · ${template.label}`;
}

function renderTemplateList() {
  const selected = currentTemplateId();
  els.templateList.innerHTML = TEMPLATES.map((template) => `
    <button class="template-tile theme-${template.id} ${template.id === selected ? "is-active" : ""}" data-template-id="${template.id}" aria-pressed="${template.id === selected}">
      <span class="template-swatch" aria-hidden="true"></span>
      <span class="template-tile-copy">
        <span class="template-tile-kicker">${escapeHtml(template.short)}</span>
        <strong>${escapeHtml(template.label)}</strong>
        <span class="template-tile-description">${escapeHtml(template.description)}</span>
      </span>
    </button>
  `).join("");

  els.templateList.querySelectorAll("[data-template-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const nextDeck = clone(state.deck);
      nextDeck.meta.templateId = button.dataset.templateId;
      nextDeck.meta.updatedAt = new Date().toISOString();
      state.deck = nextDeck;
      setDirty(true);
      render();
    });
  });
}

function renderCardList() {
  els.cardList.innerHTML = state.deck.cards
    .map((card, index) => {
      const hasIssue = state.layoutIssues.some((issue) => issue.index === index);
      return `
        <button class="deck-item ${index === state.selectedIndex ? "is-active" : ""} ${hasIssue ? "has-issue" : ""}" data-card-index="${index}">
          <span class="deck-item-index">${String(index + 1).padStart(2, "0")}</span>
          <span class="deck-item-copy">
            <span class="deck-item-title">${escapeHtml(card.title || card.id)}</span>
            <span class="deck-item-meta">${escapeHtml(cardSummary(card))}${hasIssue ? " · 需要收敛内容" : ""}</span>
          </span>
          <span class="deck-item-badge">${escapeHtml(typeLabel(card.type))}</span>
        </button>
      `;
    })
    .join("");

  els.cardList.querySelectorAll("[data-card-index]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedIndex = Number(button.dataset.cardIndex);
      render();
    });
  });
}

function renderCover(card, templateId) {
  return `
    <article class="card-frame template-${templateId} cover-card" data-export-name="${escapeHtml(card.id)}">
      <div class="card-content">
        <div class="hero-top">
          <p class="card-eyebrow">${escapeHtml(card.eyebrow)}</p>
          <h2 class="card-title">${escapeHtml(card.title)}</h2>
          <p class="card-subtitle">${escapeHtml(card.subtitle)}</p>
        </div>
        <div class="tag-row">
          ${(card.tags || []).map((tag) => `<span class="tag-chip">${escapeHtml(tag)}</span>`).join("")}
        </div>
        <div class="cover-note">
          <p>${escapeHtml(card.note)}</p>
        </div>
      </div>
    </article>
  `;
}

function renderRanking(card, templateId) {
  return `
    <article class="card-frame template-${templateId} ranking-card" data-export-name="${escapeHtml(card.id)}">
      <div class="card-content">
        <div class="hero-top">
          <p class="card-eyebrow">${escapeHtml(card.eyebrow)}</p>
          <h2 class="card-title">${escapeHtml(card.title)}</h2>
        </div>
        <div class="ranking-list">
          ${(card.rows || []).map((row, index) => `
            <div class="ranking-row">
              <span class="micro-chip">${index + 1}</span>
              <div class="ranking-main">
                <strong>${escapeHtml(row.title)}</strong>
                <span>${escapeHtml(row.subtitle)}</span>
              </div>
              <span class="stat-chip">${escapeHtml(row.stat)}</span>
            </div>
          `).join("")}
        </div>
        <div class="ranking-footer">${escapeHtml(card.note)}</div>
      </div>
    </article>
  `;
}

function renderInsight(card, templateId) {
  return `
    <article class="card-frame template-${templateId} insight-card" data-export-name="${escapeHtml(card.id)}">
      <div class="card-content">
        <div class="hero-top">
          <p class="card-eyebrow">${escapeHtml(card.eyebrow)}</p>
          <h2 class="card-title">${escapeHtml(card.title)}</h2>
        </div>
        <div class="insight-list">
          ${(card.blocks || []).map((block) => `
            <div class="insight-row">
              <div class="insight-header">
                <span class="micro-chip">${escapeHtml(block.index)}</span>
                <div class="insight-main">
                  <strong>${escapeHtml(block.title)}</strong>
                  <span>${escapeHtml(block.body)}</span>
                </div>
              </div>
            </div>
          `).join("")}
        </div>
        <div class="highlight-box">
          <strong>${escapeHtml(card.highlightTitle)}</strong>
          <span>${escapeHtml(card.highlightBody)}</span>
        </div>
      </div>
    </article>
  `;
}

function renderClosing(card, templateId) {
  return `
    <article class="card-frame template-${templateId} closing-card" data-export-name="${escapeHtml(card.id)}">
      <div class="card-content">
        <div class="hero-top">
          <p class="card-eyebrow">${escapeHtml(card.eyebrow)}</p>
          <h2 class="card-title">${escapeHtml(card.title)}</h2>
        </div>
        <div class="group-list">
          ${(card.groups || []).map((group) => `
            <div class="group-row">
              <strong>${escapeHtml(group.label)}</strong>
              <span>${escapeHtml(group.value)}</span>
            </div>
          `).join("")}
        </div>
        <div class="closing-footer">
          <span>${escapeHtml(card.footer)}</span>
          <span>${escapeHtml(card.stamp)}</span>
        </div>
      </div>
    </article>
  `;
}

function renderPreview() {
  const templateId = currentTemplateId();
  els.previewRoot.innerHTML = state.deck.cards
    .map((card, index) => {
      let inner = "";
      if (card.type === "cover") inner = renderCover(card, templateId);
      if (card.type === "ranking") inner = renderRanking(card, templateId);
      if (card.type === "insight") inner = renderInsight(card, templateId);
      if (card.type === "closing") inner = renderClosing(card, templateId);
      return `<section class="card-shell ${index === state.selectedIndex ? "is-selected" : ""}" data-preview-index="${index}">${inner}</section>`;
    })
    .join("");

  els.previewRoot.querySelectorAll("[data-preview-index]").forEach((section) => {
    section.addEventListener("click", () => {
      state.selectedIndex = Number(section.dataset.previewIndex);
      render();
    });
  });
}

function rowsToText(rows) {
  return rows.map((row) => [row.title, row.subtitle, row.stat].filter(Boolean).join(" | ")).join("\n");
}

function blocksToText(blocks) {
  return blocks.map((block) => [block.index, block.title, block.body].join(" | ")).join("\n");
}

function groupsToText(groups) {
  return groups.map((group) => [group.label, group.value].join(" | ")).join("\n");
}

function field(label, name, value, multiline = false, hint = "") {
  const input = multiline
    ? `<textarea id="${name}" name="${name}" rows="6">${escapeHtml(value)}</textarea>`
    : `<input id="${name}" name="${name}" value="${escapeHtml(value)}" />`;
  return `
    <div class="field">
      <label for="${name}">${escapeHtml(label)}</label>
      ${input}
      ${hint ? `<p class="field-hint">${escapeHtml(hint)}</p>` : ""}
    </div>
  `;
}

function editorSection(kicker, title, description, content, extraClass = "") {
  return `
    <section class="form-section ${extraClass}">
      <div class="form-section-header">
        <p class="form-section-kicker">${escapeHtml(kicker)}</p>
        <h3>${escapeHtml(title)}</h3>
        <p>${escapeHtml(description)}</p>
      </div>
      ${content}
    </section>
  `;
}

function renderEditor() {
  const card = currentCard();
  if (!card) {
    els.editorForm.innerHTML = '<div class="empty-state">没有选中的卡片。</div>';
    return;
  }

  const deckFields = `
    <div class="form-grid two-up">
      ${field("Deck 标题", "metaTitle", state.deck.meta.title || "")}
      ${field("Deck 副标题", "metaSubtitle", state.deck.meta.subtitle || "")}
    </div>
  `;

  const cardFields = `
    <div class="editor-chip-row">
      <span class="editor-chip">${escapeHtml(typeLabel(card.type))}</span>
      <span class="editor-chip subtle">第 ${String(state.selectedIndex + 1).padStart(2, "0")} 张 / 共 ${state.deck.cards.length} 张</span>
    </div>
    <div class="form-grid two-up">
      ${field("卡片 ID", "id", card.id)}
      ${field("眉题", "eyebrow", card.eyebrow || "")}
    </div>
    <div class="form-grid">
      ${field("标题", "title", card.title || "")}
    </div>
  `;

  let contentTitle = "主体文案";
  let contentDescription = "按照当前卡片类型组织内容，导出前会自动检查溢出。";
  let contentFields = "";

  if (card.type === "cover") {
    contentTitle = "封面信息";
    contentDescription = "封面负责定调，建议保留短句和强识别标签。";
    contentFields += `
      ${field("副标题", "subtitle", card.subtitle || "")}
      ${field("标签（逗号分隔）", "tags", (card.tags || []).join(", "))}
      ${field("底部摘要", "note", card.note || "", true)}
    `;
  }

  if (card.type === "ranking") {
    contentTitle = "榜单条目";
    contentDescription = "每行格式：标题 | 副标题 | 右侧数值。";
    contentFields += `
      ${field("榜单项", "rows", rowsToText(card.rows || []), true, "每行：标题 | 副标题 | 右侧数值")}
      ${field("底部总结", "note", card.note || "", true)}
    `;
  }

  if (card.type === "insight") {
    contentTitle = "趋势洞察";
    contentDescription = "每行格式：编号 | 标题 | 正文，高亮区域用于结论提炼。";
    contentFields += `
      ${field("趋势块", "blocks", blocksToText(card.blocks || []), true, "每行：编号 | 标题 | 正文")}
      ${field("高亮标题", "highlightTitle", card.highlightTitle || "")}
      ${field("高亮正文", "highlightBody", card.highlightBody || "", true)}
    `;
  }

  if (card.type === "closing") {
    contentTitle = "收尾清单";
    contentDescription = "每行格式：分组标题 | 内容，适合做行动建议或关注列表。";
    contentFields += `
      ${field("关注分组", "groups", groupsToText(card.groups || []), true, "每行：分组标题 | 内容")}
      ${field("页脚来源", "footer", card.footer || "", true)}
      ${field("页脚时间", "stamp", card.stamp || "")}
    `;
  }

  els.editorForm.innerHTML = [
    editorSection("Deck", "整组信息", "这些字段会影响整组卡片的标题和副标题。", deckFields),
    editorSection("Card", card.title || card.id, "先定卡片基础信息，再处理具体内容。", cardFields),
    editorSection("Content", contentTitle, contentDescription, `<div class="form-grid">${contentFields}</div>`, "form-section-emphasis")
  ].join("");

  els.editorForm.querySelectorAll("input, textarea").forEach((input) => {
    input.addEventListener("input", handleEditorInput);
  });
}

function parseRows(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const [title = "", subtitle = "", stat = ""] = line.split("|").map((part) => part.trim());
      return { title, subtitle, stat };
    });
}

function parseBlocks(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line, index) => {
      const [rawIndex = String(index + 1).padStart(2, "0"), title = "", body = ""] = line.split("|").map((part) => part.trim());
      return { index: rawIndex, title, body };
    });
}

function parseGroups(text) {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const [label = "", value = ""] = line.split("|").map((part) => part.trim());
      return { label, value };
    });
}

function handleEditorInput() {
  const form = new FormData(els.editorForm);
  const nextDeck = clone(state.deck);
  const card = nextDeck.cards[state.selectedIndex];

  nextDeck.meta.title = String(form.get("metaTitle") || "");
  nextDeck.meta.subtitle = String(form.get("metaSubtitle") || "");

  card.id = String(form.get("id") || card.id).trim() || card.id;
  card.eyebrow = String(form.get("eyebrow") || "");
  card.title = String(form.get("title") || "");

  if (card.type === "cover") {
    card.subtitle = String(form.get("subtitle") || "");
    card.tags = String(form.get("tags") || "")
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean);
    card.note = String(form.get("note") || "");
  }

  if (card.type === "ranking") {
    card.rows = parseRows(String(form.get("rows") || ""));
    card.note = String(form.get("note") || "");
  }

  if (card.type === "insight") {
    card.blocks = parseBlocks(String(form.get("blocks") || ""));
    card.highlightTitle = String(form.get("highlightTitle") || "");
    card.highlightBody = String(form.get("highlightBody") || "");
  }

  if (card.type === "closing") {
    card.groups = parseGroups(String(form.get("groups") || ""));
    card.footer = String(form.get("footer") || "");
    card.stamp = String(form.get("stamp") || "");
  }

  nextDeck.meta.updatedAt = new Date().toISOString();
  state.deck = nextDeck;
  setDirty(true);
  render();
}

function collectLayoutIssues() {
  const issues = [];
  const frames = [...document.querySelectorAll(".card-frame")];

  frames.forEach((frame, index) => {
    const content = frame.querySelector(".card-content");
    if (!content) return;
    const verticalOverflow = content.scrollHeight - content.clientHeight;
    const horizontalOverflow = content.scrollWidth - content.clientWidth;
    if (verticalOverflow > 2 || horizontalOverflow > 2) {
      issues.push({
        index,
        id: frame.dataset.exportName || `card-${index + 1}`,
        title: state.deck.cards[index]?.title || `Card ${index + 1}`,
        verticalOverflow: Math.max(0, Math.ceil(verticalOverflow)),
        horizontalOverflow: Math.max(0, Math.ceil(horizontalOverflow))
      });
    }
  });

  window.__LAYOUT_ISSUES__ = issues;
  return issues;
}

function renderIssueList() {
  if (!state.layoutIssues.length) {
    els.issueList.innerHTML = '<div class="empty-state success-state">当前模板下没有检测到溢出。</div>';
    return;
  }

  els.issueList.innerHTML = state.layoutIssues
    .map((issue) => `
      <div class="issue-item">
        <strong>${String(issue.index + 1).padStart(2, "0")} · ${escapeHtml(issue.title)}</strong>
        <span>纵向溢出 ${issue.verticalOverflow}px，横向溢出 ${issue.horizontalOverflow}px</span>
      </div>
    `)
    .join("");
}

function renderExports() {
  if (!state.exportRuns.length) {
    els.exportList.innerHTML = '<div class="empty-state">还没有导出记录。</div>';
    return;
  }

  els.exportList.innerHTML = state.exportRuns
    .map((run) => `
      <div class="export-run">
        <strong>${escapeHtml(run.id)}</strong>
        <div class="export-run-links">
          ${run.files.map((file) => `<a href="${file.href}" target="_blank" rel="noreferrer">${escapeHtml(file.name)}</a>`).join("")}
        </div>
      </div>
    `)
    .join("");
}

function updateLayoutState() {
  state.layoutIssues = collectLayoutIssues();
  renderIssueList();
  if (state.layoutIssues.length) {
    els.exportButton.disabled = true;
    els.exportButton.title = "当前有内容溢出，先调整文案或切换模板";
    setStatus(`发现 ${state.layoutIssues.length} 张卡片有溢出，导出已阻止。`, true);
  } else {
    els.exportButton.disabled = false;
    els.exportButton.title = "";
    setStatus(state.mode === "export" ? "导出模式已就绪" : "原型已就绪");
  }
}

function render() {
  if (!state.deck) return;
  els.app.dataset.template = currentTemplateId();
  if (state.mode === "export") {
    els.app.classList.add("is-export");
  } else {
    els.app.classList.remove("is-export");
  }
  updateHeader();
  renderTemplateList();
  renderCardList();
  renderPreview();
  if (state.mode !== "export") {
    renderEditor();
    renderExports();
  }
  updateLayoutState();
}

async function saveDeck() {
  await fetchJson("/api/deck", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(state.deck)
  });
  setDirty(false);
  setStatus("已保存到 deck.json");
}

async function exportDeck() {
  if (state.layoutIssues.length) {
    throw new Error("当前模板下仍有内容溢出，先调整后再导出。");
  }
  if (state.dirty) {
    await saveDeck();
  }
  setStatus("正在导出 1080x1440 PNG...");
  const result = await fetchJson("/api/export", { method: "POST" });
  state.exportRuns = result.runs;
  renderExports();
  setStatus(`导出完成：${result.runId}`);
}

function moveSelected(delta) {
  const nextIndex = state.selectedIndex + delta;
  if (nextIndex < 0 || nextIndex >= state.deck.cards.length) return;
  const nextDeck = clone(state.deck);
  const [card] = nextDeck.cards.splice(state.selectedIndex, 1);
  nextDeck.cards.splice(nextIndex, 0, card);
  state.deck = nextDeck;
  state.selectedIndex = nextIndex;
  setDirty(true);
  render();
}

async function boot() {
  try {
    setStatus("加载 deck.json...");
    await loadDeck();
    await loadExports();
    render();

    els.saveButton?.addEventListener("click", async () => {
      try {
        setStatus("保存中...");
        await saveDeck();
      } catch (error) {
        setStatus(error.message, true);
      }
    });

    els.reloadButton?.addEventListener("click", async () => {
      try {
        setStatus("从磁盘重载中...");
        await loadDeck();
        render();
      } catch (error) {
        setStatus(error.message, true);
      }
    });

    els.exportButton?.addEventListener("click", async () => {
      try {
        await exportDeck();
      } catch (error) {
        setStatus(error.message, true);
      }
    });

    els.moveUpButton?.addEventListener("click", () => moveSelected(-1));
    els.moveDownButton?.addEventListener("click", () => moveSelected(1));
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    window.__APP_READY__ = true;
  }
}

boot();
