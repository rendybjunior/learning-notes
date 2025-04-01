document.addEventListener("DOMContentLoaded", function () {
  let header = document.querySelector(".md-header__inner");
  let repoButton = document.querySelector(".md-header__source"); // Repo button container


  let sponsorButton = document.createElement("a");
  sponsorButton.href = "https://saweria.co/rendybjunior";
  sponsorButton.className = "md-button md-button--primary sponsor-button"; 
  sponsorButton.innerHTML = `<span class="sponsor-icon">❤️</span> Sponsor`;

  if (header) {
    if (repoButton) {
        header.insertBefore(sponsorButton, repoButton);
    } else {
        header.appendChild(sponsorButton); // Fallback if repo button is missing
    }
  }
});