const scrollToSection = (event, sectionId) => {
    event.preventDefault();
    const targetElement = document.getElementById(sectionId);
    window.scrollTo({
      top: targetElement.offsetTop,
      behavior: 'smooth'
    });
  };
export default scrollToSection;