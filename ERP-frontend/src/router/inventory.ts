import Layout from '@/layouts/index.vue';

export default [
  {
    path: '/inventory',
    name: 'inventory',
    component: Layout,
    meta: { 
        title: '库存', 
        //icon: 'user-circle' 
    },
    children: [
      {
        path: 'detail',
        name: 'inventoryDetail',
        component: () => import('@/pages/inventory/index.vue'),
        meta: { title: '库存详情' },
      },
    ],
  },
];
