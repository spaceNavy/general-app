<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : view-dash-users.vue
@Project         : general-dashboard
@Licence         : LGPL
@Description  :
-->
<template>
    <div class="view-dash-admin">
        <el-dialog :title="operate_map[dialog_status]" :visible.sync="dialogFormVisible" :close-on-click-modal="true"
                   style="margin-top: -20px;">
            <el-form :model="edit_form" label-width="100px" :rules="editFormRules" ref="editForm">
                <el-form-item label="用户名">
                    <el-input v-model="edit_form.username" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="密码">
                    <el-input v-model="edit_form.password"></el-input>
                </el-form-item>
                <el-form-item label="姓名">
                    <el-input v-model="edit_form.name"></el-input>
                </el-form-item>
                <el-form-item label="邮箱">
                    <el-input v-model="edit_form.email"></el-input>
                </el-form-item>
                <el-form-item label="电话">
                    <el-input v-model="edit_form.phone"></el-input>
                </el-form-item>
                <el-form-item label="用户角色">
                    <el-select v-model="edit_form.role_ref.name">
                        <template v-for="role in select_role_list">
                            <el-option :value="role.name">{{role.name}}</el-option>
                        </template>
                    </el-select>
                </el-form-item>

                <el-form-item label="所属机构">
                    <el-select v-model="edit_form.company_ref.name">
                        <el-option value="无">无</el-option>
                        <template v-for="company in select_company_list">
                            <el-option :value="company.name">{{company.name}}</el-option>
                        </template>
                    </el-select>
                </el-form-item>
                <el-form-item label="是否可用">
                    <el-select v-model="edit_form.is_valid">
                        <el-option value="是">是</el-option>
                        <el-option value="否">否</el-option>
                    </el-select>
                </el-form-item>

            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="dialogFormVisible=false">取消</el-button>
                <el-button v-if="dialog_status==='create'" type="primary" @click="handle_create">添加</el-button>
                <el-button v-else type="primary" @click="handle_edit">修改</el-button>
            </div>
        </el-dialog>


        <el-col class="toolbar" style="padding-bottom: 0;padding-left: 30px;margin-top: 5px;z-index: 99;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model="filters.username" placeholder="用户名"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" v-on:click="search_user">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="show_add">新增</el-button>
                </el-form-item>
            </el-form>
        </el-col>

        <div class="table-area" style="padding-bottom: 0;padding-left: 30px;overflow: auto;">
            <el-table ref="filterTable" :data="users_show" style="width: 100%" border>
                <el-table-column type="index" width="60" fixed="left"></el-table-column>
                <el-table-column prop="username" label="用户名" width="130" fixed="left"></el-table-column>
                <el-table-column prop="name" label="姓名" width="130"></el-table-column>
                <el-table-column prop="email" label="电子邮件"></el-table-column>
                <el-table-column prop="phone" label="手机"></el-table-column>
                <el-table-column prop="create_date" label="创建日期" width="150"></el-table-column>
                <el-table-column prop="role_ref.name" label="用户角色" width="110"></el-table-column>
                <el-table-column prop="company_ref.name" label="所属机构" width="110"></el-table-column>
                <el-table-column label="操作" width="100" fixed="right">
                    <template slot-scope="scope">
                        <el-button type="warning" icon="el-icon-edit" size="mini" circle
                                   @click="show_edit(scope.$index, scope.row)" title="编辑信息"></el-button>
                        <el-button type="danger" icon="el-icon-delete" size="mini" circle
                                   @click="handle_delete(scope.$index, scope.row)" title="删除用户"></el-button>
                    </template>
                </el-table-column>
            </el-table>


            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="user_current_page"
                :page-sizes="page_sizes"
                :page-size="page_sizes[0]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="user_total">
            </el-pagination>
        </div>

    </div>

</template>

<script>
    import {mapGetters} from 'vuex';
    import {app_settings} from "../settings";
    import {api_user} from "../apis";

    export default {
        name: "ViewDashAdmin",
        components: {},
        props: {},
        data() {
            return {
                page_sizes: [app_settings.defalt_count, 50, 100, 200, 300, 400],
                users_show: [],
                dialog_status: '',
                operate_map: {
                    edit: 'Edit',
                    create: 'Create'
                },
                edit_form: {
                    username: "",
                    password: "",
                    name: "",
                    email: "",
                    phone: "",
                    role: "",
                    role_ref: {name: ""},
                    company: "",
                    company_ref: {name: ""},
                    is_login: "",
                    is_valid: "",
                },
                dialogFormVisible: false,
                editFormRules: {
                    username: [{required: true, message: '请输入姓名', trigger: 'blur'}]
                },
                filters: {
                    "username": ""
                },
                current_id: 0,
                current_index: 0,
                role_name_id_map: {},
                company_name_id_map: {},
                select_role_list: [],
                select_company_list: [],
            }
        },
        methods: {

            handleSizeChange(val) {
                this.$store.dispatch("set_page_count_from_view", val).then(() => {
                    this.get_user_list(1, this.user_page_count)
                });
            },
            handleCurrentChange(val) {
                this.get_user_list(val, this.user_page_count)
            },

            search_user() {

            },

            get_user_list(current_page, count) {
                this.$store.dispatch(
                    "get_user_list",
                    {
                        current_page: current_page,
                        count: count,
                    }).then(() => {
                    this.$notify({
                        title: '信息拉取成功',
                        message: '用户列表拉取成功',
                        type: 'success',
                        duration: 500
                    });
                    this.make_show_info();
                    this.select_user_dict_for_user = {};
                    for (let user of this.users) {
                        let key = user.username + "-" + user.name;
                        this.select_user_dict_for_user[key] = user.uid;
                    }
                }).catch(() => {
                    this.$notify({
                        title: '用户列表拉取失败',
                        type: 'error',
                        duration: 3000
                    });
                });
            },
            make_show_info() {
                this.users_show = [];
                this.select_user_for_user = [];
                for (let user of this.users) {
                    let temp = {
                        uid: user.uid,
                        username: user.username,
                        name: user.name,
                        email: user.email,
                        phone: user.phone,
                        role: user.role,
                        role_ref: user.role_ref,
                        create_date: user.create_time.substring(0, 16),
                        company: user.company,
                        company_ref: user.company_ref,
                        is_valid: user.is_valid ? "是" : "否",
                        key: user.username + "-" + user.name
                    };
                    if (Object.prototype.toString.call(user.company_ref) !== '[object Object]') {
                        temp.company_ref = {name: ""};
                    }
                    this.users_show.push(temp);
                    if (user.username !== this.current_user.username) {
                        this.select_user_for_user.push(temp);
                    }
                }
            },

            get_role_list() {
                this.$store.dispatch(
                    "get_role_list",
                    {
                        current_page: 1,
                        count: 0,
                    }).then(response => {
                        this.select_role_list = response.data.data;
                        this.role_name_id_map = {};
                        for (let role of this.select_role_list) {
                            this.role_name_id_map[role.name] = role.uid;
                        }
                }).catch(() => {
                    this.$notify({
                        title: '角色列表拉取失败',
                        type: 'error',
                        duration: 3000
                    });
                });
            },
            get_company_list() {
                this.$store.dispatch(
                    "get_company_list",
                    {
                        current_page: 1,
                        count: 0,
                    }).then(response => {
                        this.select_company_list = response.data.data;
                        this.company_name_id_map = {};
                        for (let company of this.select_company_list) {
                            this.company_name_id_map[company.name] = company.uid;
                        }
                }).catch(() => {
                    this.$notify({
                        title: '使用机构列表拉取失败',
                        type: 'error',
                        duration: 3000
                    });
                });
            },

            // 显示新增界面
            show_add() {
                this.dialog_status = 'create';
                this.dialogFormVisible = true;
                this.edit_form = {
                    username: "",
                    password: "",
                    name: "",
                    phone: "",
                    email: "",
                    role: "",
                    role_ref: {name: ""},
                    company: "",
                    company_ref: {name: "无"},
                    is_valid: "是",
                    is_login: false
                }
            },
            // 显示编辑界面
            show_edit(index, row) {
                this.current_id = row.uid;
                this.current_index = index;
                this.dialog_status = 'edit';
                this.dialogFormVisible = true;
                this.edit_form = Object.assign({}, row);
            },

            // 新增
            handle_create() {
                this.$confirm('确定新增用户?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.dialogFormVisible = false;
                    let form_temp = JSON.parse(JSON.stringify(this.edit_form));
                    form_temp.role = this.role_name_id_map[form_temp.role_ref.name];
                    if (form_temp.company_ref.name === "无" || form_temp.company_ref.name === "") {
                        form_temp.company = "";
                    } else {
                        form_temp.company = this.company_name_id_map[form_temp.company_ref.name]
                    }
                    form_temp.is_valid = form_temp.is_valid === "是";
                    api_user.add_user(form_temp).then(() => {
                        this.$notify({
                            title: '用户添加成功',
                            type: 'success',
                            duration: 500
                        });
                        this.get_user_list(1, this.user_page_count);
                    }).catch(() => {
                        this.$notify({
                            title: '添加用户失败',
                            type: 'error',
                            duration: 3000
                        });
                    });
                }).catch(() => {
                    this.$notify({
                        title: '已取消添加用户。',
                        message: "",
                        type: 'info',
                        duration: 500
                    });
                });
            },
            // 编辑
            handle_edit() {
                this.$confirm('确定修改用户信息?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.dialogFormVisible = false;
                    let form_temp = JSON.parse(JSON.stringify(this.edit_form));
                    form_temp.role = this.role_name_id_map[form_temp.role_ref.name];
                    form_temp.is_valid = form_temp.is_valid === "是";
                    for (let i in form_temp) {
                        if (form_temp[i] === "" || form_temp[i] === null || form_temp[i] === undefined) {
                            delete form_temp[i]
                        }
                    }
                    if (form_temp.company_ref.name === "无" || form_temp.company_ref.name === "") {
                        form_temp.company = "";
                    } else {
                        form_temp.company = this.company_name_id_map[form_temp.company_ref.name]
                    }
                    delete form_temp.create_date;

                    api_user.edit_user(this.current_id, form_temp).then(() => {
                        this.$notify({
                            title: '用户修改成功',
                            type: 'success',
                            duration: 500
                        });
                        this.get_user_list(1, this.user_page_count);
                    }).catch(() => {
                        this.$notify({
                            title: '修改用户失败',
                            type: 'error',
                            duration: 2000
                        });
                    });
                }).catch(() => {
                    this.$notify({
                        title: '已取消修改用户。',
                        message: "",
                        type: 'info',
                        duration: 500
                    });
                });
            },
            // 删除
            handle_delete(index, row) {
                this.$confirm('此操作将删除用户, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    api_user.remove_user(row.uid).then(() => {
                        this.$notify({
                            title: '用户删除成功',
                            message: '删除的用户：' + row.username,
                            type: 'success',
                            duration: 500
                        });
                        this.get_user_list(1, this.user_page_count);
                    }).catch(() => {
                        this.$notify({
                            title: '删除用户失败',
                            type: 'error',
                            duration: 2000
                        });
                    });
                }).catch(() => {
                    this.$notify({
                        title: '已取消删除',
                        message: "",
                        type: 'info',
                        duration: 500
                    });
                });
            },
        },
        created() {
            this.get_user_list(1, this.user_page_count);
            this.get_role_list(); // 获取所有的角色
            this.get_company_list();
        },
        mounted() {

        },
        computed: {
            ...mapGetters([
                "current_user",
                "users",
                "user_total",
                "user_page_count",
                "user_current_page",
            ]),
        },
        watch: {},
        destroyed() {

        },

    }
</script>

<style scoped>
    * {
        box-sizing: border-box;
        position: relative;
    }

    .view-dash-admin {
        width: 100%;
        height: 100%;
        overflow: auto;
    }
</style>
