import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            users: []
        };
    },
    methods: {
        onAddUserClick(){
            this.$router.push('/admin/edit-user/new');
        },

        getUsers() {
            axios.get('/users', {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.users = res.data;
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        },

        editUser(user_id){
            this.$router.push('/admin/edit-user/' + user_id);
        },
        deleteUser(user_id){
            if (!confirm('Do you want to delete user?')){
                return;
            }
            axios.delete('/users/' + user_id, {
                headers: {
                    'Token': Token.token,
                }
            })
            .then((res) => {
                this.getUsers();
            })
            .catch((error) => {
              console.log(error.response.data);
            })
        }
    },
    mounted() {
        this.getUsers();
    },
    template: `
        <button id="add-user" v-on:click="onAddUserClick">Add user</button>
        <table id="users-list">
            <tr>
                <th>id</th>
                <th>full name</th>
                <th>job title</th>
                <th>cathedra</th>
                <th>role</th>
                <th>login</th>
                <th>email</th>
                <th></th>
                <th></th>
            </tr>
            <tr class="user-item" v-for="(item, index) in users" v-bind:id="item.id" v-bind:key="item.id">
                <td>{{ item.id }}</td>
                <td>{{ item.full_name }}</td>
                <td>{{ item.job_title }}</td>
                <td>{{ item.cathedra }}</td>
                <td>{{ item.role }}</td>
                <td>{{ item.login }}</td>
                <td>{{ item.email }}</td>
                <td v-on:click="editUser(item.id)">Edit</td>
                <td v-on:click="deleteUser(item.id)">Delete</td>
            </tr>
        </table>
    `,
};