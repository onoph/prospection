(() => {
  console.log('Script de suivi de profil chargé !');
  const checkAndFollow = () => {
    const followButton = Array.from(document.querySelectorAll('button.follow'))
      .find(btn => btn.getAttribute('aria-label') === 'Suivre');

    if (followButton && !followButton.disabled) {
      followButton.click();
      console.log("✅ Bouton Suivre cliqué.");
    } else {
      setTimeout(checkAndFollow, 1000);
    }
  };

  checkAndFollow();
})();