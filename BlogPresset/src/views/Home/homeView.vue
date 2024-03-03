<script setup>
import base_url from "../../constant/index";
import AppMenu from "../../components/AppMenu.vue";
import LeftSideView from "../../components/home/LeftSideView.vue";
import RightSideView from "../../components/home/RightSideView.vue";
import { onBeforeMount, ref } from "vue";

const email = sessionStorage.getItem("email");
const posts = ref({});
const comments = ref("");
const current_post_val = ref({});
const current_post = ref({});
const target = ref("");
const charged = ref(false);
const current_post_id  = ref(0)

onBeforeMount(() => {
  fetch(`${base_url}/all_posts_with_comments`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const new_data = [];
      for (let i = 0; i < data.total_posts * 1; i++) {
        new_data.push(data.all_posts_with_comments[`post${i + 1}`]);
      }
      posts.value = new_data.reverse();
      // console.log(posts.value)
    })
    .catch((error) => {
      console.error("Error fetching posts with comments:", error);
    });
});

const addComments = async () => {
  const data = {
    comments: comments.value,
  };
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };
  try {
    const response = await fetch(
      `${base_url}/add_comments/${email}/${current_post_id.value}`,
      options
    );
    const jsonResponse = await response.json();
    if (jsonResponse.success) {
      // console.log(jsonResponse);
      localStorage.setItem('post', "")
      window.location.reload();
    } else {
      console.error("Error adding comment:", jsonResponse.message);
    }
  } catch (error) {
    console.error("Error adding comment:", error);
  }
};

const setId = (post_id) => {
  current_post_id.value = post_id * 1;
};

const setComment = async (post) => {
  current_post_val.value = await post;
  localStorage.setItem('post', JSON.stringify(post));
  window.location.reload()
};

const updateComment = (id) => {
  alert(id);
};
const deleteComment = (id) => {
  alert(id);
};
</script>

<template>
  <section id="container">
    <AppMenu :act="1" />
    <section id="corps">
      <LeftSideView />
      <section id="blog" v-if="posts !== {}">
        <div class="userCard"></div>
        <div class="articles" v-for="post in posts" :key="post">
          <div class="article">
            <div class="author">
              <div class="image">
              <img
                v-if="post.profile"
                :src="post.profile"
                alt=""
                width="50"
                style="
                  margin-top: -6px;
                  border: 1px solid;
                  border-radius: 50%;
                "
              />
              </div>
              <div class="userInfo">
                <h2 style="padding-top: 20px">@{{ post.pseudo }}</h2>
                <p style="padding-top: 6px">
                  <a :href="'mailto:' + post.email"
                    >Send an email to the author</a
                  >
                </p>
              </div>
            </div>
            <div class="userPost">
              <p>{{ post.post }}</p>
            </div>
            <p style="font-size: 11px; font-style: italic">
              Article added on {{ post.created_at.split("GMT")[0] }}
            </p>
            <div class="reactions">
              <div
                id="pouce"
                data-toggle="modal"
                data-target="#addComment"
                @click="setId(post.post_id)"
              >
                <img src="../../assets/messager.png" alt="" width="22" />
              </div>
              <div
                class="all"
                data-toggle="modal"
                :data-target="target"
                @click="setComment(post)"
              >
                <p>All comments {{ post.comments.length }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal -->
        <div
          class="modal fade"
          id="addComment"
          tabindex="-1"
          role="dialog"
          aria-labelledby="addPostCentertitre"
          aria-hidden="true"
          ref="addPostModal"
        >
          <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-titre" id="addPostLongtitre">Comment post</h5>
                <button
                  type="button"
                  class="close"
                  data-dismiss="modal"
                  aria-label="Close"
                >
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <div class="postArea">
                  <p style="font-size: 13px; margin-bottom: 0px">
                    Your comment here (max 225 characters)
                  </p>
                  <br />
                  <textarea id="tArea" rows="7" v-model="comments"></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button id="addPostButtton" @click="addComments">
                  Add comment
                </button>
              </div>
            </div>
          </div>
        </div>

        <div
          class="modal fade bd-example-modal-lg"
          tabindex="-1"
          role="dialog"
          aria-labelledby="myLargeModalLabel"
          aria-hidden="true"
          v-if="charged"
        >
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div
                class="articles"
                v-if="Object.keys(current_post).length !== 0"
              >
                <div class="article">
                  <div class="author">
                    <div class="image">
                      <img
                        :src="current_post.profile"
                        alt=""
                        width="50"
                        style="
                          margin-top: -6px;
                          border: 1px solid;
                          border-radius: 50%;
                        "
                      />
                    </div>
                    <div class="userInfo">
                      <h2 style="padding-top: 20px">
                        @{{ current_post.pseudo }}
                      </h2>
                    </div>
                  </div>
                  <div class="userPost">
                    <p>{{ current_post.post.slice(0, 250) + "..." }}</p>
                  </div>
                  <p style="font-size: 11px; font-style: italic">
                    Article added on
                    {{ current_post.created_at.split("GMT")[0] }}
                  </p>
                </div>
                <p style="margin-left: 20px">All comments</p>
                <div class="comments">
                  <div
                    class="comment"
                    v-for="comment in current_post.comments.reverse()"
                    :key="comment"
                  >
                    <div class="auth">
                      <div>
                        <img
                          :src="comment.profile"
                          width="40"
                          style="border: 1px solid; border-radius: 50%"
                        />
                      </div>
                      <div>
                        <div style="margin-left: 10px; font-size: 12px">
                          <p
                            v-if="comment.comment_email !== email"
                            style="margin-top: -20px"
                          >
                            @{{ comment.username }}
                          </p>
                          <p v-else>You</p>
                        </div>
                        <div style="margin-left: 10px">
                          <p
                            v-if="comment.comment_email !== email"
                            style="
                              margin-top: 0px;
                              font-size: 11px;
                              color: blue;
                            "
                          >
                            <a :href="'mailto:' + comment.comment_email"
                              >Send an email to the author</a
                            >
                          </p>
                        </div>
                      </div>
                    </div>
                    <div class="comm" style="margin-left: 50px">
                      <p style="font-size: 13px; margin-top: -4px">
                        "{{ comment.comments }}"
                      </p>
                      <p
                        v-if="comment.comment_email === email"
                        style="cursor: pointer"
                        @click="updateComment(comment.comment_id)"
                      >
                        Modifier
                      </p>
                      <p
                        v-if="comment.comment_email === email"
                        style="cursor: pointer"
                        @click="deleteComment(comment.comment_id)"
                      >
                        &times;
                      </p>
                      <p
                        style="
                          font-size: 8px;
                          font-style: italic;
                          text-align: right;
                          padding-right: 15px;
                          margin-top: -5px;
                        "
                      >
                        Comment add on {{ comment.created_at.split("GMT")[0] }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section id="blog" v-else>
        <p style="text-align:center; font-size:20px; opacity:.5; margin-top:320px">Nothing to show now ! Please add post</p>
      </section>
      <RightSideView/>
    </section>
    <router-view />
  </section>
</template>

<style scoped>
.comments {
  border: 1px solid #adadad;
  margin: 20px;
  border-radius: 10px;
}
.comment {
  background-color: #d5d5d5;
  padding: 10px;
  border-radius: 10px;
  margin: 10px;
}
.auth {
  display: flex;
  justify-content: start;
  align-items: center;
}
.auth p {
  position: absolute;
  margin-top: -10px;
}
#corps {
  display: flex;
  width: 100%;
  flex-direction: row;
  overflow: hidden;
}
#blog {
  width: 55%;
  background-color: #fff;
  margin-top: 20px;
  height: 88vh;
  overflow: scroll;
  color: #000;
  border-radius: 10px;
}
.article {
  padding: 20px;
  margin: 20px;
  border: 1px solid #d7d7d7;
  border-radius: 10px;
}
.author {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
.userInfo h2 {
  margin-left: 10px;
  font-size: 15px;
  margin-top: -3px;
}
.userInfo p {
  font-size: 12px;
  margin-top: -10px;
  margin-left: 10px;
}
.userPost p {
  text-align: justify;
  font-size: 15px;
}
.threeImage,
.oneImage,
.twoImage {
  display: flex;
  justify-content: center;
  align-items: center;
}
#one {
  width: 260px;
  margin-right: 40px;
  margin-bottom: 20px;
}
#two,
#three {
  width: 120px;
  margin-left: 40px;
  margin-bottom: 20px;
}
.twoImage img,
.oneImage img {
  width: 120px;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
.reactions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
#pouce img {
  margin-right: 40px;
  cursor: pointer;
}
.all p {
  cursor: pointer;
  color: rgb(98, 98, 220);
}

#pouce img:hover,
.all p:hover {
  opacity: 0.5;
  color: #787878;
}
</style>
