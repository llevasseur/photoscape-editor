import React from 'react'

const Button = ({ id, className, setChoice, backgroundImages, choice }) => {
  const handleClick = () => {
    setChoice(choice === id ? '' : id)
  }

  // Conditionally apply a different class based on whether the button's ID matches the choice state
  const buttonClass = id === choice ? 'selected' : ''

  return (
    <button
      className={`${className} ${buttonClass}`}
      onClick={handleClick}
      style={{
        backgroundImage:
          className === 'single-image-button'
            ? `url(${backgroundImages[0]})`
            : `none`,
      }}
    >
      {/* Only use the div below if {className} === 'double-image-button'*/}
      {className === 'double-image-button' && (
        <div className="image-container">
          <div
            className="image1"
            style={{ backgroundImage: `url(${backgroundImages[0]})` }}
          ></div>
          <div
            className="image2"
            style={{ backgroundImage: `url(${backgroundImages[1]})` }}
          ></div>
        </div>
      )}
    </button>
  )
}

export default Button
