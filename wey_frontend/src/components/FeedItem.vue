<!-- components/FeedItem.vue -->
<template>
    <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-6">
            <img :src="post.created_by.get_avatar" class="w-[40px] rounded-full">
            
            <p>
                <strong>
                    <RouterLink :to="{name: 'profile', params:{'id': post.created_by.id}}">{{ post.created_by.name }}</RouterLink>
                </strong>
            </p>
        </div>

        <p class="text-gray-600">{{ post.created_at_formatted }} ago</p>
    </div>

        <template v-if="post.attachments.length">
            <template v-for="attachment in post.attachments">
                <template v-if="isImage(attachment.get_file)">
                    <img :src="attachment.get_file" class="w-full mb-4 rounded-xl">
                </template>
                <template v-else-if="isVideo(attachment.get_file)">
                    <video controls class="w-full mb-4 rounded-xl" autoplay loop muted>
                        <source :src="attachment.get_file">
                        Ваш браузер не поддерживает видео.
                    </video>
                </template>
            </template>
        </template>


    <p><strong>{{ post.body }}</strong></p>

    <div class="my-6 flex justify-between">
        <div class="flex space-x-6">

            <!-- LIKE -->
            <div class="flex items-center space-x-2" @click="likePost(post.id)">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"></path>
                </svg>    
                <span class="text-gray-500 text-xs">{{ post.likes_count }} лайков</span>
            </div>
            <!-- END_LIKE -->

            <!-- COMMENT -->
            <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z"></path>
                </svg> 
                <RouterLink :to="{name: 'postview', params: {id: post.id}}" class="text-gray-500 text-xs">{{ post.comments_count }} комментов</RouterLink>
            </div>
            <!-- END_COMMENT -->

            <!-- REPOST -->
            <div class="flex items-center space-x-2" @click="repostPost(post.id)">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.593 3.322c1.1.128 1.907 1.077 1.907 2.185V21L12 17.25 4.5 21V5.507c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0111.186 0z" />
                </svg>
                <span class="text-gray-500 text-xs">{{ post.reposts_count }} репостов</span>
            </div>
            <!-- END_REPOST -->

        </div>
        
        <div>
            <!-- DELETE_POST -->
            <div @click="toggleExtraModal">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"></path>
                </svg> 
            </div> 
            <!-- END_DELETE_POST -->
        </div>
    </div>
    
    <!-- Доп окно -->
    <div v-if="showExtraModal">
        <div class="flex space-x-6 items-center">

            <div 
                class="flex items-center space-x-2" 
                @click="deletePost"
                v-if="userStore.user.id === post.created_by.id"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                </svg>
                <span class="text-red-500 text-xs">Удалить пост</span>   
            </div>
        </div>
    </div>
    <!-- END_Доп окно -->
    
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'

export default {
    emits: ['deletePost'],
    props: {
        post: Object
    },

    setup() {
        const userStore = useUserStore()

        return {
            userStore,
        }
    },

    data() {
        return {
            showExtraModal: false
        }
    },

    components: { RouterLink },

    methods: {
        likePost(id) {
            axios
                .post(`/api/posts/${id}/like/`)
                .then(response => {
                    if (response.data.message === "like created") {
                        
                        this.post.likes_count += 1;
                    }
                })
                .catch(error => {
                    console.log("error", error);
                });
        },

        repostPost() {
            axios
                .post(`/api/posts/${this.post.id}/repost/`)
                .then(response => {
                    if (response.data.message === "repost created") {
                        this.post.reposts_count += 1;
                    }
                })
                .catch(error => {
                    console.log("error", error);
                });
        },

        deletePost() {
            this.$emit('deletePost', this.post.id)

            axios
                .delete(`/api/posts/${this.post.id}/delete/`)
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.log("error", error);
                });

        },

        toggleExtraModal() {
            this.showExtraModal = !this.showExtraModal
        },
        isImage(url) {
            const imageExtensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg',];
            const extension = url.split('.').pop().toLowerCase();
            return imageExtensions.includes(extension);
        },

        isVideo(url) {
            const videoExtensions = ['mp4', 'avi', 'mkv', 'mov',];
            const extension = url.split('.').pop().toLowerCase();
            return videoExtensions.includes(extension);
        },
    },
}

</script>
