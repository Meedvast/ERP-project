import Layout from '@/layouts/index.vue';

export default [
  {
    path: '/conduct',
    name: 'conduct',
    component: Layout,
    meta: {
      title: '产品',
      // icon: 'user-circle'
    },
    children: [
      {
        path: 'detail',
        name: 'conductDetail',
        component: () => import('@/pages/product/index.vue'),
        meta: { title: '产品详情' },
      },
    ],
  },
];
