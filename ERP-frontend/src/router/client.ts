import Layout from '@/layouts/index.vue';

export default [
  {
    path: '/client',
    name: 'client',
    component: Layout,
    meta: { 
        title: '客户', 
        //icon: 'user-circle' 
    },
    children: [
      {
        path: 'detail',
        name: 'clientDetail',
        component: () => import('@/pages/client/index.vue'),
        meta: { title: '客户详情' },
      },
    ],
  },
];
