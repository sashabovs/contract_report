
import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            users: [],
        };
    },
    methods: {
        onAddUserClick(){
            console.log(Token.token);
        }
    },
    template: `
        <button id="add-user" v-on:click="onAddUserClick">Add user</button>
        <ol id="users-list">
            <li class="user-item" v-for="(item, index) in users" v-bind:id="index">
                {{ item.id }}
            </li>
        </ol>
    `,
};