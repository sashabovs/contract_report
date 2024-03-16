
import Token from './Token.js'

export default {
    components: {

    },
    data() {
        return {
            users: [],
            isEditingUser: false,
            isAddingNew:false,
            user: {},
            passwordVal:"",
            job_titles: [],
            cathedras: [],
            roles: []
        };
    },
    methods: {
        addUser(){
            this.isEditingUser = true;
            this.user = {};
            this.passwordVal = "";
            this.isAddingNew = true;
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

        editUser(user){
            this.isEditingUser = true;
            this.isAddingNew = false;
            this.user = {"id":user.id, "full_name":user.full_name, "job_title":user.job_title,
            "cathedra":user.cathedra, "role":user.role, "login":user.login, "email":user.email};
            this.passwordVal = "";
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
        },
        save() {
            let body = {"user": this.user, "password": this.passwordVal}
            if(this.isAddingNew){
                axios.post('/users/' + this.id,body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.getUsers();
                    this.isEditingUser = false;
                    this.isAddingNew = false;
                    this.user = {};
                    this.passwordVal = "";
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }else{
                axios.put('/users/' + this.user.id, body, {
                    headers: {
                        'Token': Token.token,
                    }
                })
                .then((res) => {
                    this.getUsers();
                    this.isEditingUser = false;
                    this.isAddingNew = false;
                    this.user = {};
                    this.passwordVal = "";
                })
                .catch((error) => {
                  console.log(error.response.data);
                })
            }

        },
        cancel() {
            this.getUsers();
            this.isEditingUser = false;
            this.isAddingNew = false;
            this.user = {};
            this.passwordVal = "";
        },
    },
    mounted() {
        this.getUsers();

        axios.get('/job_titles', {
            headers: {
                'Token': Token.token,
            }
        })
        .then((res) => {
            this.job_titles = res.data;
        })
        .catch((error) => {
          console.log(error.message);
        })

        axios.get('/cathedras', {
            headers: {
                'Token': Token.token,
            }
        })
        .then((res) => {
            this.cathedras = res.data;
        })
        .catch((error) => {
          console.log(error.response.data);
        })

        axios.get('/roles', {
            headers: {
                'Token': Token.token,
            }
        })
        .then((res) => {
            this.roles = res.data;
        })
        .catch((error) => {
          console.log(error.response.data);
        })

    },
    template: `
        <div class="centered-div">
            <button id="add-user" v-on:click="addUser">Add user</button>
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
                    <td v-on:click="editUser(item)">Edit</td>
                    <td v-on:click="deleteUser(item.id)">Delete</td>
                </tr>
            </table>

            <div class="modal-background" v-show="isEditingUser">
                <div class="fully-centered-div" id='edit-report'>
                    <label for="id">id:</label>
                    <input id="id" required v-model="user.id">

                    <label for="full-name">Full name:</label>
                    <input id="full-name" required v-model="user.full_name">

                    <label for="job-title">Job title:</label>
                    <select name="job-title" id="job-title" v-model="user.job_title_id">
                          <option value=""></option>
                          <option v-bind:value="item.id" v-for="(item, index) in job_titles" v-bind:key="item.id">{{ item.name }}</option>
                    </select>

                    <label for="cathedra">Cathedra:</label>
                    <select name="cathedra" id="cathedra" v-model="user.cathedra_id">
                          <option value=""></option>
                          <option v-bind:value="item.id" v-for="(item, index) in cathedras" v-bind:key="item.id">{{ item.name }}</option>
                    </select>

                    <label for="role">Role:</label>
                    <select name="role" id="role" v-model="user.role">
                          <option value=""></option>
                          <option v-bind:value="item" v-for="(item, index) in roles" v-bind:key="item">{{ item }}</option>
                    </select>

                    <label for="login">Login:</label>
                    <input id="login" required v-model="user.login">

                    <label for="password">New password:</label>
                    <input id="password" type="password" v-model="passwordVal">

                    <label for="email">Email:</label>
                    <input id="email" required v-model="user.email">

                    <button v-on:click="save">Save</button>
                    <button v-on:click="cancel">Cancel</button>
                </div>
            </div>

        </div>
    `,
};