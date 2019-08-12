<!--
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : view-dash-company.vue
@Project         : general-dashboard
@Licence         : LGPL
@Description  :
 -->

<template>
    <div class="view-dash-company">
        <el-dialog :title="operate_map[dialog_status]" :visible.sync="dialogFormVisible" :close-on-click-modal="false"
                   style="margin-top: -20px;">
            <el-form :model="edit_form" label-width="120px" ref="editForm">
                <el-form-item label="机构名称">
                    <el-input v-model="edit_form.name" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="机构描述">
                    <el-input v-model="edit_form.comment"></el-input>
                </el-form-item>
                <el-form-item label="机构负责人">
                    <el-select v-model="edit_form.leader">
                        <template v-for="user in select_leader_list">
                            <el-option :value="user.key">{{user.key}}</el-option>
                        </template>
                    </el-select>
                </el-form-item>
                <el-form-item label="机构售后">
                    <el-select v-model="edit_form.seller">
                    <template v-for="user in select_seller_list">
                        <el-option :value="user.key">{{user.key}}</el-option>
                    </template>
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
                    <el-button type="primary" v-on:click="search_role">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="show_add">新增</el-button>
                </el-form-item>
            </el-form>
        </el-col>

        <div class="table-area" style="padding-bottom: 0;padding-left: 30px;overflow: auto;">
            <el-table ref="filterTable" :data="companies_show" style="width: 90%" border>
                <el-table-column type="index" width="50" fixed="left"></el-table-column>
                <el-table-column prop="name" label="机构名称" width="150"></el-table-column>
                <el-table-column prop="leader_ref.name" label="负责人" width="150"></el-table-column>
                <el-table-column prop="comment" label="描述" width="150"></el-table-column>
                <el-table-column prop="seller_ref.name" label="售后" width="150"></el-table-column>
                <el-table-column prop="create_time" label="创建日期" ></el-table-column>
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
                :current-page="company_current_page"
                :page-sizes="page_sizes"
                :page-size="page_sizes[0]"
                layout="total, sizes, prev, pager, next, jumper"
                :total="company_total">
            </el-pagination>
        </div>

    </div>

</template>

<script>
    import {mapGetters} from 'vuex';
    import {app_settings} from "../settings";
    import {api_company} from "../apis";

    export default {
        name: "ViewDashCompany",
        components: {},
        props: {},
        data() {
            return {
                page_sizes: [app_settings.defalt_count, 50, 100, 200, 300, 400],
                companies_show: [],

                dialog_status: '',
                operate_map: {
                    update: 'Edit',
                    create: 'Create'
                },
                edit_form: {
                    name: "",
                    leader: "",
                    comment: "",
                    seller: "",
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
                select_leader_list: [],
                select_seller_list: [],
                user_key_id_map: {},
            }
        },
        methods: {

            handleSizeChange(val) {
                this.$store.dispatch("set_page_count_from_view", parseInt(val)).then(() => {
                    this.get_company_list(1, this.company_page_count)
                });
            },
            handleCurrentChange(val) {
                this.get_company_list(parseInt(val), this.company_page_count)
            },

            search_role() {

            },

            // 获取数据并存储
            get_company_list(current_page, count) {
                this.$store.dispatch(
                    "get_company_list",
                    {
                        current_page: current_page,
                        count: count,
                    }).then(() => {
                    this.$notify({
                        title: 'Company拉取成功',
                        message: 'Company列表拉取成功',
                        type: 'success',
                        duration: 2000
                    });
                    this.make_show_info();
                }).catch(() => {
                    this.$notify({
                        title: 'Company列表拉取失败',
                        type: 'error',
                        duration: 3000
                    });
                });
            },
            make_show_info() {
                this.companies_show = [];
                for (let company of this.companies) {
                    let temp = {
                        uid: company.uid,
                        name: company.name,
                        leader: company.leader_ref.username + "-" + company.leader_ref.name,
                        create_time: company.create_time.substring(0, 16),
                        comment: company.comment,
                        seller: company.seller_ref.username + "-" + company.seller_ref.name,
                        leader_ref: company.leader_ref,
                        seller_ref: company.seller_ref,
                    };
                    this.companies_show.push(temp);
                }
            },

            get_user_list(current_page, count) {
                this.$store.dispatch(
                    "get_user_list",
                    {
                        current_page: current_page,
                        count: count,
                    }).then(() => {
                    this.user_key_id_map = {};
                    this.select_leader_list = [];
                    this.select_seller_list = [];
                    for (let user of this.users) {
                        let key = user.username + "-" + user.name;
                        this.user_key_id_map[key] = user.uid;
                        if (user.role_ref.code === app_settings.role_custom_leader|| user.role_ref.code === app_settings.role_custom_employee) {
                            this.select_leader_list.push({
                                "key": key
                            });
                        }
                        if (user.role_ref.code === app_settings.role_manager || user.role_ref.code === app_settings.role_seller) {
                            this.select_seller_list.push({
                                "key": key
                            });
                        }
                    }
                }).catch(() => {
                    this.$notify({
                        title: '用户列表拉取失败',
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
                    name: "",
                    leader: "",
                    comment: "",
                    seller: "",
                }
            },
            // 显示编辑界面
            show_edit(index, row) {
                this.current_id = row.uid;
                this.current_index = index;
                this.dialog_status = 'update';
                this.dialogFormVisible = true;
                this.edit_form = Object.assign({}, row);
                this.edit_form.leader = this.edit_form.leader_ref
            },

            // 新增
            handle_create() {
                this.$confirm('确定新增公司?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.dialogFormVisible = false;
                    let form_temp = JSON.parse(JSON.stringify(this.edit_form));
                    form_temp.leader = this.user_key_id_map[form_temp.leader];
                    form_temp.seller = this.user_key_id_map[form_temp.seller];
                    api_company.add_company(form_temp).then(() => {
                        this.$notify({
                            title: '公司添加成功',
                            type: 'success',
                            duration: 1000
                        });
                        this.get_company_list(1, this.company_page_count);
                    }).catch(() => {
                        this.$notify({
                            title: '添加用户公司',
                            type: 'error',
                            duration: 2000
                        });
                    });
                }).catch(() => {
                    this.$notify({
                        title: '已取消添加公司。',
                        message: "",
                        type: 'info',
                        duration: 1000
                    });
                });
            },
            // 编辑
            handle_edit() {
                this.$confirm('确定修改公司信息?', '提示', {
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
                    form_temp.leader = this.user_key_id_map[form_temp.leader];
                    form_temp.seller = this.user_key_id_map[form_temp.seller];
                    api_company.edit_company(this.current_id, form_temp).then(() => {
                        this.$notify({
                            title: '角色修改成功',
                            type: 'success',
                            duration: 1000
                        });
                        this.get_company_list(1, this.company_page_count);
                    }).catch(() => {
                        this.$notify({
                            title: '修改公司失败',
                            type: 'error',
                            duration: 2000
                        });
                    });
                }).catch(() => {
                    this.$notify({
                        title: '已取消修改公司。',
                        message: "",
                        type: 'info',
                        duration: 1000
                    });
                });
            },
            // 删除
            handle_delete(index, row) {
                this.$confirm('此操作将删除该公司, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    api_company.remove_company(row.uid).then(() => {
                        this.$notify({
                            title: '公司删除成功',
                            message: '删除的公司：' + row.name,
                            type: 'success',
                            duration: 1000
                        });
                        this.get_company_list(1, this.company_page_count);
                    }).catch(() => {
                        this.$notify({
                            title: '删除机构失败',
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
            this.get_company_list(1, this.company_page_count);
            this.get_user_list(1, 0);
        },
        mounted() {

        },
        computed: {
            ...mapGetters([
                "companies",
                "company_total",
                "company_page_count",
                "company_current_page",
                "users",
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

    .view-dash-company {
        width: 100%;
        height: 100%;
        overflow: auto;
    }
</style>
