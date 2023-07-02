import { defineStore } from 'pinia';

import { getUserInfo } from '@/api/list';
import { usePermissionStore } from '@/store';
import type { UserInfo } from '@/types/interface';

const InitUserInfo: UserInfo = {
  name: '', // 用户名，用于展示在页面右上角头像处
  roles: [], // 前端权限模型使用 如果使用请配置modules/permission-fe.ts使用
};

export const useUserStore = defineStore('user', {
  state: () => ({
    token: 'main_token', // 默认token不走权限
    userInfo: { ...InitUserInfo },
  }),
  getters: {
    roles: (state) => {
      return state.userInfo?.roles;
    },
  },
  actions: {
    // eslint-disable-next-line consistent-return
    async login(userInfo: Record<string, string>) {
      console.log(`用户信息:`, userInfo);
      const { name, password } = userInfo;
      const result = await getUserInfo(name, password);
      if (result === 400) {
        return {
          code: 400,
          message: '账号不存在',
        };
      }
      if (result === 401) {
        return {
          code: 401,
          message: '密码错误',
        };
      }
      /*         const token = {
          main_: 'main_token',
          dev_: 'dev_token',
        }[password]; */
      if (result === 200) {
        return {
          code: 200,
          message: '登陆成功',
          data: 'main_token',
        };
      }
    },
    /*       const res = await mockLogin(userInfo);
      if (res.code === 200) {
        this.token = res.data;
      } else {
        throw res;
      }
    }, */
    async getUserInfo() {
      const mockRemoteUserInfo = async (token: string) => {
        if (token === 'main_token') {
          return {
            name: 'Tencent',
            roles: ['all'], // 前端权限模型使用 如果使用请配置modules/permission-fe.ts使用
          };
        }
        return {
          name: 'td_dev',
          roles: ['UserIndex', 'DashboardBase', 'login'], // 前端权限模型使用 如果使用请配置modules/permission-fe.ts使用
        };
      };
      const res = await mockRemoteUserInfo(this.token);

      this.userInfo = res;
    },
    /*     async logout() {
      this.token = '';
      this.userInfo = { ...InitUserInfo };
    }, */
  },
  persist: {
    afterRestore: () => {
      const permissionStore = usePermissionStore();
      permissionStore.initRoutes();
    },
    key: 'user',
    paths: ['token'],
  },
});
