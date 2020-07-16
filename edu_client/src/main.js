// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from "axios";
import store from './store/index'

Vue.prototype.$axios = axios;
import Element from "element-ui"
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(Element);
import settings from "./settings";
// 导入极验
import "../static/js/gt.js"
Vue.prototype.$settings = settings;
Vue.config.productionTip = false;
import "../static/css/global.css"
require('video.js/dist/video-js.css');
require('vue-video-player/src/custom-theme.css');
import VideoPlayer from 'vue-video-player'

Vue.use(VideoPlayer);
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
})
