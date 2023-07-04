import Layout from '@/layouts/index.vue';

export default [
  {
    path: '/order',
    component: Layout,
    name: 'order',
    redirect: '/order/index.vue',
    meta: {
      title: '订单',
      // icon: shallowRef(DashboardIcon),
    },
    children: [
      {
        path: 'index',
        name: 'OrderDetail',
        component: () => import('@/pages/order/index.vue'),
        meta: {
          title: '订单详情',
        },
      },
    ],
  },
];
