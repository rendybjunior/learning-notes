document.addEventListener("DOMContentLoaded", function () {
    let header = document.querySelector(".md-header__inner");
    if (header) {
      // Sponsor Button
      let sponsorButton = document.createElement("a");
      sponsorButton.href = "https://saweria.co/rendybjunior"; // Change URL
      sponsorButton.className = "md-button md-button--primary sponsor-button"; 
      sponsorButton.innerHTML = `
        <span class="sponsor-icon">❤️</span> Sponsor
      `;
  
      // GitHub Star Button
      let starButton = document.createElement("a");
      starButton.href = "https://github.com/rendybjunior/praktisdbt/stargazers"; // Change to your repo's Stargazers page
      starButton.className = "md-button md-button--primary star-button"; 
      starButton.innerHTML = `
        <span class="star-icon">⭐</span> Star
      `;
  
      // Append buttons to the header
      header.appendChild(sponsorButton);
    //   header.appendChild(starButton);
    }
  });