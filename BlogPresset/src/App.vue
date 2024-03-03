<script setup>
import {ref} from 'vue';
const width = ref(window.innerWidth);
window.addEventListener('resize', () => {
  width.value = window.innerWidth;
});
</script>

<template>
  <div v-if="width >= 1250" >
    <router-view></router-view>
  </div>
  <div v-else class="mobile">
    <p>
      Veuillez vous mettre sur un écran plus large pour une meilleure experience
      utilisateur pour l'instant. <br />Nous travaillons encore sur la version mobile. <br> Merci pour votre compréhension 🙏
    </p>
  </div>
</template>

<style scoped>
.mobile{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
  font-size: 15px;
  font-weight: bold;
}
.mobile p{
  border: 1px solid;
  padding: 10px;
  border-radius: 10px;
  background-color: #fff;
}
</style>
