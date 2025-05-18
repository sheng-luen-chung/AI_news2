// 讀取 JSONL 檔案
async function loadArticles() {
  try {
    const response = await fetch("news.jsonl");
    const text = await response.text();
    // 將 JSONL 文字分割成行並解析每一行，並按時間戳倒序排列
    return text
      .trim()
      .split("\n")
      .map((line) => JSON.parse(line))
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
  } catch (error) {
    console.error("載入文章失敗:", error);
    return [];
  }
}

// 建立音訊播放列表
function createAudioList(articles) {
  return articles.map((article) => {
    const authors = Array.isArray(article.authors)
      ? article.authors.join("、")
      : article.authors;
    return {
      name: article.title_zh,
      artist: authors,
      url: article.audio,
      cover:
        "https://raw.githubusercontent.com/DIYgod/APlayer/master/assets/default.jpg",
    };
  });
}

// 建立文章 HTML
function createArticleHTML(article) {
  const authors = Array.isArray(article.authors)
    ? article.authors.join("、")
    : article.authors;
  return `
        <div class="article">
            <div class="title">
                <a class="title-original" href="${article.url}" target="_blank" style="display:none;">${article.title}</a>
                <a class="title-translation" href="${article.url}" target="_blank">${article.title_zh}</a>
            </div>
            <div class="meta">${authors} ｜ ${article.published_date}</div>
            <div class="abstract">
                <span class="abstract-original" style="display:none;">${article.summary}</span>
                <span class="abstract-translation">${article.summary_zh}</span>
            </div>
        </div>
    `;
}

// 初始化頁面
async function initializePage() {
  const articles = await loadArticles();

  // 初始化音訊播放器
  const ap = new APlayer({
    container: document.getElementById("aplayer"),
    audio: createAudioList(articles),
    theme: "#6366f1",
    lrcType: 0,
    listFolded: false,
    listMaxHeight: 200,
    order: "list",
    controls: ["prev", "play", "next", "progress", "volume", "list"],
  });

  // 顯示文章
  const container = document.getElementById("articles-container");
  container.innerHTML = articles.map(createArticleHTML).join("");
}

// 切換中英文顯示
let showingTranslation = true;
function toggleAll() {
  showingTranslation = !showingTranslation;
  const btn = document.getElementById("toggle-all-btn");
  document
    .querySelectorAll(".title-original")
    .forEach((e) => (e.style.display = showingTranslation ? "none" : ""));
  document
    .querySelectorAll(".title-translation")
    .forEach((e) => (e.style.display = showingTranslation ? "" : "none"));
  document
    .querySelectorAll(".abstract-original")
    .forEach((e) => (e.style.display = showingTranslation ? "none" : ""));
  document
    .querySelectorAll(".abstract-translation")
    .forEach((e) => (e.style.display = showingTranslation ? "" : "none"));
  btn.textContent = showingTranslation ? "顯示原文" : "顯示翻譯";
}

// 當頁面載入完成時初始化
document.addEventListener("DOMContentLoaded", initializePage);
