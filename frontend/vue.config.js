// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true
// })

// module.exports = {
//   configureWebpack: {
//     // Add the following to enable or disable feature flags
//     plugins: [
//       new webpack.DefinePlugin({
//         '__VUE_OPTIONS_API__': true, // or false
//         '__VUE_PROD_DEVTOOLS__': false,
//         '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': false, // add this line
//       })
//     ]
//   }
// };

const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        '__VUE_OPTIONS_API__': true, // or false
        '__VUE_PROD_DEVTOOLS__': false,
        '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': false,
      })
    ]
  }
});
