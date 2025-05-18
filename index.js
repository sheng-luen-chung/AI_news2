// 讀取 JSONL 檔案
async function loadArticles() {
  try {
    const response = await fetch("news.jsonl");
    const text = await response.text();
    // 將 JSONL 文字分割成行並解析每一行，直接反轉順序
    return text
      .trim()
      .split("\n")
      .map((line) => JSON.parse(line))
      .reverse(); // 直接反轉陣列順序，最新的文章會在最前面
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
        <div class="article" data-audio-id="${article.id}">
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

  // 監聽播放器事件
  function updateCurrentArticle() {
    const currentAudio = ap.list.audios[ap.list.index];
    const currentId = currentAudio.url.split("/").pop().replace(".mp3", "");

    // 移除所有文章的 playing 類別
    document.querySelectorAll(".article").forEach((article) => {
      article.classList.remove("playing");
    });

    // 為當前播放的文章添加 playing 類別
    const currentArticle = document.querySelector(
      `.article[data-audio-id="${currentId}"]`
    );
    if (currentArticle) {
      currentArticle.classList.add("playing");
      // 平滑滾動到當前文章
      setTimeout(() => {
        currentArticle.scrollIntoView({ behavior: "smooth", block: "center" });
      }, 300);
    }
  }

  // 監聽播放和切換曲目事件
  ap.on("play", updateCurrentArticle);
  ap.on("listswitch", updateCurrentArticle);
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
