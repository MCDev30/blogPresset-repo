<template>
  <section v-if="post !== ''">
  <div class="card">
      <p v-if="post.email !== email" style="text-align:center; padding:10px; font-weight:bold; border-bottom:1px solid #cecece">All comments with post of @{{ post.pseudo }}</p>
      <p v-else style="text-align:center; padding:10px; font-weight:bold; border-bottom:1px solid #cecece">All comments of your post</p>
      <div style="display:flex; justify-content:flex-start; align-items:center">
        <img :src="post.profile" width="40" style="border:1px solid #cecece; border-radius:50%; margin-left:10px">
        <p v-if="post.email !== email" style="margin-top:1px; position:absolute; left:55px">@{{ post.pseudo }}</p>
        <p v-else style="margin-top:15px; position:absolute; left:55px">You</p>
      </div>
      <p v-if="post.email == !email" style="position:absolute; left:55px; top:85px; font-size:11px"> <a :href="'mailto:' + post.email">Send an email to the author</a></p>
      <p style="width:300px; font-size:13px; padding:10px; text-align:justify; margin-left:5px; ">{{ post.post.slice(0, 250) + '...' }}</p>
      <p style="text-align:right; font-size:8px; margin-right:30px; margin-bottom:20px; margin-top:-15px; font-style:italic">{{ post.created_at.split("GMT")[0] }}</p>
      <hr>
      <div class="comment" v-for="com in post.comments" :key="com" style="padding:10px; background-color:#cecece; margin:10px; width:300px; border-radius:10px;">

        <p v-if="com.comment_email == email" style="font-size:20px; cursor:pointer; position:absolute; right:25px; color:red" @click="deleteComment(com.comment_id)">&times;</p>
        <img v-if="com.comment_email == email" src="../../assets/refresh.png" width="13" style="cursor:pointer; position:absolute; right:55px; margin-top:10px" @click="setCommentInfos(com.comment_id, com.comments)" data-toggle="modal" data-target="#update">

        <div style="display:flex; margin-bottom:10px;">
          <img :src="com.profile" width="40" height="40"  style="border:1px solid #cecece; border-radius:50%;">
          <p v-if="com.comment_email !== email" style="margin-top:2px; position:absolute; left:65px; font-size:13px; color:blue">@{{ com.username }}</p>
          <p v-else style="margin-top:10px; position:absolute; left:65px;">You</p>
          <p v-if="com.comment_email !== email" style="margin-top:22px; position:absolute; left:65px; font-size:12px">{{ com.comment_email }}</p>
        </div>
        <p style="width:250px; font-size:11px; text-align:justify; padding:10px;; margin-top:-15px; margin-left:35px; font-weight:bold;">{{ com.comments }}</p>
        <p style="font-size:8px; text-align:right; margin-top:-20px; font-style: italic;">{{ com.created_at }}</p>
      </div>

          <!-- Modal -->
          <div class="modal fade" id="update" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title" id="exampleModalLongTitle">Update comment</h5>
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
                  <textarea  rows="7" v-model="updated" style="background-color:#fff; color:#000; width:100%; padding:10px; border-radius:10px"></textarea>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                  <button type="button" class="btn btn-primary" @click="updateComment">Save changes</button>
                </div>
              </div>
            </div>
          </div>



  </div>
  </section>
  <section v-else>
    <div class="card">
      <p style="padding:20px; width:300px; margin-top:300px; text-align:center; opacity:.4">Click "All comments" to see all comments relative to the post here</p>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import base_url from '../../constant';
const post = localStorage.getItem('post')? JSON.parse(localStorage.getItem('post')): "";
const email = sessionStorage.getItem("email")
const updated = ref('')
const setCommentInfos = (id, comment) => {
  localStorage.setItem("comment_id", id)
  localStorage.setItem("comment", comment)
  updated.value = comment
}

const deleteComment = (id) => {
  fetch(`${base_url}/delete_comments/${id}`, {
    method: 'DELETE'
  })
  .then(response => {
    if (response.ok) {
      alert('Comment deleted successfully');
      localStorage.setItem('post', "")
      window.location.reload();
    } else {
      alert('Failed to delete comment. Try again !!');
    }
  })
  .catch(error => {
    console.error('Error deleting comment:', error);
    alert('An error occurred while deleting the comment');
  });
}

const updateComment = () => {
  const id = localStorage.getItem('comment_id') * 1
  fetch(`${base_url}/update_comments/${email}/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      comments: updated.value
    })
  })
  .then(response => {
    if (response.ok) {
      localStorage.setItem('post', "")
      window.location.reload()
    } else {
      alert('Failed to update comment. Try again !!');
    }
  })
  .catch(error => {
    console.error('Error updating comment:', error);
    alert('An error occurred while updating the comment');
  });
}
</script>

<style scoped>
.card{
  background-color: #fffcfc;
  margin: 20px;
  border-radius: 10px;
  overflow-y: scroll;
  color: #000;
  height: 88vh;
}

</style>
