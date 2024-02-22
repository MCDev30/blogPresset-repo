<script setup>
import { ref } from "vue";
import base_url from "../constant";
defineProps({
  act: Number,
});

const error = ref("")

const logout = async () => {
  const data = {
    email: sessionStorage.getItem('email'),
    token: sessionStorage.getItem('token')
  };
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };
  try {
    const response = await fetch(`${base_url}/logout`, options);
    const jsonResponse = await response.json();
    if (jsonResponse.status === 200) {
      sessionStorage.clear()
      error.value = jsonResponse.message
      window.location.replace('/')
    } else {
      error.value = jsonResponse.message
    }
  } catch (error) {
    console.error("Erreur lors de la requête :", error);
    throw error;
  }
};
</script>

<template>
  <section id="menus">
    <div class="log">
      <div class="avata" style="cursor: pointer">
        <h4>BP</h4>
      </div>
      <div class="search">
        <img src="../assets/icons8-search-50.png" alt="" width="17" />
        <input type="text" id="search_input" placeholder="Search..." />
      </div>
    </div>

    <div class="menu_lin">
      <ul>
        <router-link to="/home">
          <li :class="[act == 1 ? 'activ' : '']">
            <img src="../assets/home.png" alt="" width="25" />
          </li>
        </router-link>

        <router-link to="/">
          <li :class="[act == 2 ? 'activ' : '']">
            <img src="../assets/cloche.png" alt="" width="25" />
          </li>
        </router-link>

        <router-link to="/profile">
          <li :class="[act == 3 ? 'activ' : '']">
            <img src="../assets/utilisateur.png" alt="" width="25" />
          </li>
        </router-link>
      </ul>
    </div>

    <div class="separator"></div>
    <router-link to="/">
      <div class="dashboard">
        <img src="../assets/tableau-de-bord.png" alt="" width="30" />
      </div>
    </router-link>

    <div data-toggle="modal" data-target="#exampleModal">
      <div
        data-toggle="tooltip"
        data-placement="bottom"
        title="Se déconnecter"
        style="margin-left: 50px; cursor: pointer"
      >
        <img src="../assets/logout.png" alt="" width="30" />
      </div>
    </div>

    <!-- Modal -->
    <div
      class="modal fade"
      id="exampleModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Blog Presset</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body" v-if="error === ''">
            Voulez-vous vraiment vous déconnecter ? <br />Confirmez pour vous
            déconnecter
          </div>
          <div class="modal-body" v-else>
            {{ error }}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="logout">
              Se déconnecter
            </button>
            <button type="button" class="btn btn-danger" data-dismiss="modal">
              Annuler
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style>
#menus {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
  box-shadow: 1px 1px 0px #0000000c;
  padding: 20px;
  height: 60px;
}
.activ {
  border-bottom: 4px solid rgb(98, 98, 220);
  padding-bottom: 6px;
}
.log {
  display: flex;
  justify-content: center;
  align-items: center;
}
.menu_lin ul {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px;
}
.avata h4 {
  color: #fff;
  background-color: rgb(98, 98, 220);
  padding: 5px;
  border-radius: 2px;
  padding-left: 7px;
  padding-right: 7px;
  margin: 20px;
}
.search {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  background-color: #8594f356;
  padding: 2px;
  height: 37px;
  width: 300px;
  border-radius: 3px;
}
.search img {
  margin-left: 10px;
  margin-right: 10px;
}
.search input {
  background-color: transparent;
  border: none;
  outline: none;
  width: 100%;
  padding: 2px;
  height: 30px;
  font-size: 16px;
  color: #000;
}
.menu_lin li {
  list-style: none;
  margin: 20px;
  cursor: pointer;
  width: 50px;
  text-align: center;
  transition: ease-in-out 0.2s;
  /* padding-bottom: 6px; */
}
.menu_lin li:hover {
  border-bottom: 2px solid rgb(129, 129, 129);
  opacity: 0.6;
  padding-bottom: 6px;
}
.separator {
  height: 35px;
  width: 2px;
  background-color: #00000056;
  margin: 20px;
  margin-left: -20px;
}
</style>
