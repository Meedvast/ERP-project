import Layout from '@/layouts/index.vue';

export default [
  {
    path: '/order',
    name: 'order',
    component: Layout,
    meta: { 
        title: '订单', 
        //icon: 'user-circle' 
    },
    children: [
      {
        path: 'detail',
        name: 'orderdetail',
        component: () => import('@/pages/order/index.vue'),
        meta: { title: '订单详情' },
      },
    ],
  },
];
