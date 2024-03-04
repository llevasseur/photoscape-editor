import React from 'react'
import './Logo.css'

const Logo = () => {
  const handleClick = () => {
    const url = 'https://www.nuckstalk.com/instagram-posts'
    window.open(url, '_blank')
  }
  return (
    <div className="logo-container clickable">
      <img
        draggable="false"
        src="./android-chrome-512x512.png"
        alt="Nucks Talk Logo 512x512"
        onClick={handleClick}
      ></img>
    </div>
  )
}

export default Logo
