

<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.get_avatar" class="mb-6 rounded-full">
                
                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">{{ user.friends_count }} друзья</p>
                    <p class="text-xs text-gray-500">{{ user.posts_count }} посты</p>
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-if="friendshipRequests.length"
            >
                <h2 class="mb-6 text-xl"><strong>Запросы на дружбу</strong></h2>

                <div 
                    class="p-4 mt-4 text-center bg-gray-100 rounded-lg"
                    v-for="friendshipRequest in friendshipRequests"
                    v-bind:key="friendshipRequest.id"
                >
                    <img :src="friendshipRequest.created_by.get_avatar" class="w-[200px] mb-4 mx-auto rounded-full">
                
                    <p>
                        <strong>
                            <RouterLink :to="{name: 'profile', params:{'id': friendshipRequest.created_by.id}}">{{ friendshipRequest.created_by.name }}</RouterLink>
                        </strong>
                    </p>

                    <div class="mt-4 flex space-x-4 justify-around">
                        <p class="text-xs text-gray-500">{{ user.friends_count }} друзья</p>
                        <p class="text-xs text-gray-500">{{ user.posts_count }} посты</p>
                    </div>

                    <div class="mt-4 space-x-4">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg" @click="handleRequest('accepted', friendshipRequest.created_by.id)">Принимать</button>
                        <button class="inline-block py-4 px-6 bg-red-600 text-white rounded-lg" @click="handleRequest('rejected', friendshipRequest.created_by.id)">Отказать</button>
                    </div>
                    
                </div>
            </div>

            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-2 gap-4"
                v-if="friends.length"
            >
                <h2 class="mb-2 text-xl col-span-2"><strong>Друзья</strong></h2>
                <div 
                    class="p-4 text-center bg-gray-100 rounded-lg"
                    v-for="user in friends"
                    v-bind:key="user.id"
                >
                    <img :src="user.get_avatar" class="mb-6 rounded-full">
                
                    <p>
                        <strong>
                            <RouterLink :to="{name: 'profile', params:{'id': user.id}}">{{ user.name }}</RouterLink>
                        </strong>
                    </p>

                    <div class="mt-6 flex space-x-8 justify-around">

                        <p class="text-xs text-gray-500">{{ user.friends_count }} друзья</p>
                        <p class="text-xs text-gray-500">{{ user.posts_count }} посты</p>

                    </div>
                </div>
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <Trends />
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Trends from '../components/Trends.vue'
import { useUserStore } from '@/stores/user'

export default {
    name: 'FriendsView',

    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    components: {
        Trends
    },

    data() {
        return {
            user: {},
            friendshipRequests: [],
            friends: [],
        }
    },

    mounted() {
        this.getFriends()
    },

    methods: {
        getFriends() {
            axios
                .get(`/api/friends/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.friendshipRequests = response.data.requests
                    this.friends = response.data.friends
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        handleRequest(status, pk) {
            console.log('handleRequest', status)

            const friendIndex = this.friendshipRequests.findIndex(request => request.created_by.id === pk);
            const friend = this.friendshipRequests[friendIndex].created_by;

            if (status === 'accepted') {
                this.friends.push(friend);
                this.user.friends_count++;
            }

            this.friendshipRequests.splice(friendIndex, 1);

            axios
                .post(`/api/friends/${pk}/${status}/`)
                .then(response => {
                    console.log('data', response.data)
                    this.getFriends()
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>


