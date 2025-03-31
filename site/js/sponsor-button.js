document.addEventListener("DOMContentLoaded", function () {
    let header = document.querySelector(".md-header__inner");
    if (header) {
      let starButton = document.createElement("div");
      starButton.className = "github-star-button";
      starButton.innerHTML = `
        <a class="github-button" href="https://github.com/rendybjunior/praktisdbt" data-icon="octicon-star" data-size="large" aria-label="Star YOUR_USERNAME/YOUR_REPOSITORY on GitHub">Star</a>
      `;
      header.appendChild(starButton);
    }
  });