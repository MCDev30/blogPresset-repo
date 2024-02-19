<script setup>

import base_url from '../../constant/index'
import AppMenu from "../../components/AppMenu.vue";
import LeftSideView from "../../components/home/LeftSideView.vue";
import RightSideView from "../../components/home/RightSideView.vue";

const username = sessionStorage.getItem('username')
const email = sessionStorage.getItem('email')
const token = sessionStorage.getItem('token')
const profile = sessionStorage.getItem('profile')


</script>

<template>
  <section id="container">
    <AppMenu :act="3" />
    <section id="corps">
      <section id="profile">
        <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Similique, inventore vero saepe consequatur excepturi deserunt accusamus amet sapiente iusto provident cum rerum, reprehenderit ullam labore sit. Modi dolorem fugiat amet?</p>
      </section>
      <section id="other">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Eaque explicabo porro eos at earum illum pariatur asperiores, corrupti rem accusamus, vitae ex doloribus esse fuga. Architecto nisi iure fugiat mollitia!
      </section>

    </section>
    <router-view />
  </section>
</template>

<style scoped>
#corps {
  display: flex;
  padding-left: 130px;
  padding-right: 130px;
}
#profile, #other{
  background-color: #fff;
  margin-top: 20px;
  height: 88vh;
  overflow: scroll;
  color: #000;
  border-radius: 10px;
  margin-left: 0px;
}
#other{
    width: 600px;
    margin-left: 30px;
}
</style>
