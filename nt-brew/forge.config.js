module.exports = {
  packagerConfig: {
    icon: 'public/icons/icon',
  },
  asar: {
    unpack: ['**/backend/dist/**/*', '**/public/**/*'],
  },
  rebuildConfig: {},
  makers: [
    {
      name: '@electron-forge/maker-squirrel',
      config: {},
    },
    {
      name: '@electron-forge/maker-dmg',
      platforms: ['darwin'],
      config: {},
    },
  ],
}
