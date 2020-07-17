<template>
  <div class="cart_item">
    <div class="cart_column column_1">
      <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
    </div>
    <div class="cart_column column_2">
      <img src="../../../static/image/python.png" alt="">
      <span><router-link :to="'/course/detail/'+course.id">{{course.name}}</router-link></span>
    </div>
    <div class="cart_column column_3">
      <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
        <el-option :label="item.expire_text" :value="item.id" :key="item.id" v-for="item in course.expire_list"></el-option></el-select>
    </div>
    <div class="cart_column column_4">{{course.real_price}}</div>
    <div class="cart_column column_4" @click="del">删除</div>
  </div>
</template>


<script>
  export default {
    name: "CartItem",
    props: ["course"],
    watch: {
      'course.selected': function () {
        this.change_select()
      },
      'course.expire_id':function () {
        this.change_expire()
      }
    },
    methods: {
      del() {
        let token = localStorage.user_token || sessionStorage.user_token;
        this.$axios.delete(`${this.$settings.HOST}cart/option/`, {
          selected: this.course.selected,
          course_id: this.course.id,
        }, {
          headers: {
            "Authorization": "jwt " + token,
          }
        }).then(response => {
          this.$message.success(response.data.message);
          window.reload()
        }).catch(error => {
          this.$message.error(error.response)
        })
      },
      change_select() {
        let token = localStorage.user_token || sessionStorage.user_token;
        this.$axios.patch(`${this.$settings.HOST}cart/option/`, {
          selected: this.course.selected,
          course_id: this.course.id,
        }, {
          headers: {
            "Authorization": "jwt " + token,
          }
        }).then(response => {
          this.$message.success(response.data.message);
        }).catch(error => {
          this.$message.error(error.response)
        })
      },
      change_expire(){
        let token = localStorage.user_token || sessionStorage.user_token;
        this.$axios.put(`${this.$settings.HOST}cart/option/`,{
          expire_id:this.course.expire_id,
          course_id:this.course.id
        },{
          headers:{
            "Authorization": "jwt " + token,
          }
        }).then(response=>{
          console.log(response.data);
          this.course.real_price = response.data.real_price
          // location.reload()
        }).catch(error=>{
          console.log(error)
        })
      },
    },
    data() {
      return {
        expire: "1个月有效"
      }
    }
  }
</script>

<style scoped>
  .cart_item::after {
    content: "";
    display: block;
    clear: both;
  }

  .cart_column {
    float: left;
    height: 250px;
  }

  .cart_item .column_1 {
    width: 88px;
    position: relative;
  }

  .my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
  }

  .cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 116px;
  }

  .cart_item .column_2 img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
  }

  .cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
  }

  .my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
  }

  .cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
  }

</style>
