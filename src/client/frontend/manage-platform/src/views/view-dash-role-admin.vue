<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : view-dash-role-admin.vue
@Project         : general-dashboard
@Licence         : LGPL
@Description  :
 -->

<template>
    <div class="view-dash-role-admin">
        <el-dialog :title="operate_map[dialog_status]" :visible.sync="dialogFormVisible" :close-on-click-modal="false"
                   style="margin-top: -20px;">
            <el-form :model="edit_form" label-width="80px" ref="editForm">
                <el-form-item label="角色名称">
                    <el-input v-model="edit_form.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="角色代码">
                    <el-input v-model="edit_form.code"></el-input>
                </el-form-item>
                <el-form-item label="角色级别">
                    <el-input v-model="edit_form.level"></el-input>
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
                    <el-button type="primary" v-on:click="search_role">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="show_add">新增</el-button>
                </el-form-item>
            </el-form>
        </el-col>

        <div class="table-area" style="padding-bottom: 0;padding-left: 30px;overflow: auto;">
            <el-table ref="filterTable" :data="roles_show" style="width: 90%" border>
                <el-table-column type="index" width="50" fixed="left"></el-table-column>
                <el-table-column prop="name" label="角色名称" width="150"></el-table-column>
                <el-table-column prop="code" label="角色代码" width="150"></el-table-column>
                <el-table-column prop="level" label="角色等级" width="150"></el-table-column>
                <el-table-column prop="create_time" label="创建日期" ></el-table-column>
                <el-table-column label="操作" width="100" fixed="right">
                    <template slot-scope="scope">
                        <el-button type="warning" icon="el-icon-edit" size="mini" circle
                                   @click="show_edit(scope.$index, scope.row)" title="编辑信息"></el-button>
                        <el-button type="danger" icon="el-icon-delete" size="mini" circle
                                   @click="handle_delete(scope.$index, scope.row)" title="删除信息"></el-button>
                    </template>
                </el-table-column>
            </el-table>


            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="1"
                :page-sizes="page_sizes"
                :page-size="page_sizes[0]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="role_total">
            </el-pagination>
        </div>

    </div>

</template>

<script>
    import {mapGetters} from 'vuex';
    import {app_settings} from "../settings";
    import {api_role} from "../apis";

    export default {
        name: "ViewDashRoleAdmin",
        components: {},
        props: {},
        data() {
            return {
                page_sizes: [app_settings.defalt_count, 50, 100, 200, 300, 400],
                roles_show: [],

                dialog_status: '',
                operate_map: {
                    update: 'Edit',
                    create: 'Create'
                },
                edit_form: {
                    name: "",
                    code: "",
                    level: 100,
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
            }
        },
        methods: {


            handleSizeChange(val) {
                this.$store.dispatch("set_page_count_from_view", val).then(() => {
                    this.get_role_list(1, this.role_page_count)
                });
            },
            handleCurrentChange(val) {
                this.get_role_list(val, this.role_page_count)
            },

            search_role() {

            },

            // 获取数据并存储
            get_role_list(current_page, count) {
                this.$store.dispatch(
                    "get_role_list",
                    {
                        current_page: current_page,
                        count: count,
                    }).then(() => {
                    this.$notify({
                        title: '信息拉取成功',
                        message: '角色列表拉取成功',
                        type: 'success',
                        duration: 800
                    });
                    this.make_show_info();
                }).catch(() => {
                    this.$notify({
                        title: '角色列表拉取失败',
                        type: 'error',
                        duration: 3000
                    });
                });
            },
            make_show_info() {
                this.roles_show = [];
                for (let role of this.roles) {
                    let temp = {
                        uid: role.uid,
                        name: role.name,
                        code: role.code,
                        level: role.level,
                        create_time: role.create_time
                    };
                    this.roles_show.push(temp);
                }
            },

            // 显示新增界面
            show_add() {
                this.dialog_status = 'create';
                this.dialogFormVisible = true;
                this.edit_form = {
                    name: "",
                    code: "",
                    level: 0,
                }
            },
            // 显示编辑界面
            show_edit(index, row) {
                this.current_id = row.uid;
                this.current_index = index;
                this.dialog_status = 'update';
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
                    form_temp.level = parseInt(form_temp.level);
                    api_role.add_role(form_temp).then(() => {
                        this.$notify({
                            title: '用户添加成功',
                            type: 'success',
                            duration: 1000
                        });
                        this.get_role_list(1, this.role_page_count);
                    }).catch(() => {
                        this.$notify({
                            title: '添加用户失败',
                            type: 'error',
                            duration: 2000
                        });
                    });
                }).catch(() => {
                    this.$notify({
                        title: '已取消添加用户。',
                        message: "",
                        type: 'info',
                        duration: 1000
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
                    for (let i in form_temp) {
                        if (form_temp[i] === "" || form_temp[i] === null || form_temp[i] === undefined) {
                            delete form_temp[i]
                        }
                    }
                    delete form_temp.create_date;
                    form_temp.level = parseInt(form_temp.level);
                    api_role.edit_role(this.current_id, form_temp).then(() => {
                        this.$notify({
                            title: '角色修改成功',
                            type: 'success',
                            duration: 1000
                        });
                        this.get_role_list(1, this.role_page_count);
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
                        duration: 1000
                    });
                });
            },
            // 删除
            handle_delete(index, row) {
                this.$confirm('此操作将删除该角色, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    api_role.remove_role(row.uid).then(() => {
                        this.$notify({
                            title: '角色删除成功',
                            message: '删除的角色：' + row.name,
                            type: 'success',
                            duration: 1000
                        });
                        this.get_role_list(1, this.role_page_count);
                    }).catch(() => {
                        this.$notify({
                            title: '删除角色失败',
                            type: 'error',
                            duration: 2000
                        });
                    });
                }).catch(() => {
                    this.$notify({
                        title: '已取消删除',
                        message: "",
                        type: 'info',
                        duration: 1000
                    });
                });
            },
        },
        created() {
            this.get_role_list(1, this.role_page_count)
        },
        mounted() {

        },
        computed: {
            ...mapGetters([
                "roles",
                "role_total",
                "role_page_count",
                "role_current_page",
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

    .view-dash-role-admin {
        width: 100%;
        height: 100%;
        overflow: auto;
    }
</style>
