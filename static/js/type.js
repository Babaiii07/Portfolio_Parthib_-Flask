document.addEventListener("DOMContentLoaded", function() {
  const typewriter = document.querySelector('.typewriter');
  const phrases = ["Python Backend Developer", "Machine Learning Enthusiast", "Android Developer"];
  let phraseIndex = 0;
  let letterIndex = 0;
  let typingDelay = 100;
  let erasingDelay = 50;
  let newPhraseDelay = 2000; // Delay before starting next phrase

  function type() {
    if (letterIndex < phrases[phraseIndex].length) {
      typewriter.textContent += phrases[phraseIndex].charAt(letterIndex);
      letterIndex++;
      setTimeout(type, typingDelay);
    } else {
      setTimeout(erase, newPhraseDelay);
    }
  }

  function erase() {
    if (letterIndex > 0) {
      typewriter.textContent = phrases[phraseIndex].substring(0, letterIndex - 1);
      letterIndex--;
      setTimeout(erase, erasingDelay);
    } else {
      phraseIndex = (phraseIndex + 1) % phrases.length;
      setTimeout(type, typingDelay);
    }
  }

  type();
});
