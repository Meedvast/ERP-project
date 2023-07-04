<!-- eslint-disable prettier/prettier -->
<!-- eslint-disable prettier/prettier -->
<!-- eslint-disable prettier/prettier -->
<template>
  <div class="list-common-table">
    <t-form ref="form" :data="formData" :label-width="80" colon @reset="onReset" @submit="onSubmit">
      <t-row>
        <t-col :span="10">
          <t-row :gutter="[24, 24]">
            <t-col :span="4">
              <t-form-item label="合同名称" name="name">
                <t-input
                  v-model="formData.name"
                  class="form-item-content"
                  type="search"
                  placeholder="请输入合同名称"
                  :style="{ minWidth: '134px' }"
                />
              </t-form-item>
            </t-col>
            <t-col :span="4">
              <t-form-item label="合同状态" name="status">
                <t-select
                  v-model="formData.status"
                  class="form-item-content"
                  :options="CONTRACT_STATUS_OPTIONS"
                  placeholder="请选择合同状态"
                />
              </t-form-item>
            </t-col>
            <t-col :span="4">
              <t-form-item label="合同编号" name="no">
                <t-input
                  v-model="formData.no"
                  class="form-item-content"
                  placeholder="请输入合同编号"
                  :style="{ minWidth: '134px' }"
                />
              </t-form-item>
            </t-col>
            <t-col :span="4">
              <t-form-item label="合同类型" name="type">
                <t-select
                  v-model="formData.type"
                  style="display: inline-block"
                  class="form-item-content"
                  :options="CONTRACT_TYPE_OPTIONS"
                  placeholder="请选择合同类型"
                />
              </t-form-item>
            </t-col>
          </t-row>
        </t-col>

        <t-col :span="2" class="operation-container">
          <t-button theme="primary" type="submit" :style="{ marginLeft: 'var(--td-comp-margin-s)' }"> 查询 </t-button>
          <t-button type="reset" variant="base" theme="default"> 重置 </t-button>
        </t-col>
      </t-row>
    </t-form>

    <div class="table-container">
      <t-table
        :data="data"
        :columns="COLUMNS"
        :row-key="rowKey"
        :vertical-align="verticalAlign"
        :hover="hover"
        :pagination="pagination"
        :loading="dataLoading"
        :header-affixed-top="headerAffixedTop"
        @page-change="rehandlePageChange"
        @change="rehandleChange"
      >
        <template #status="{ row }">
          <t-tag v-if="row.status === CONTRACT_STATUS.FAIL" theme="danger" variant="light"> 审核失败 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.AUDIT_PENDING" theme="warning" variant="light"> 待审核 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.EXEC_PENDING" theme="warning" variant="light"> 待履行 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.EXECUTING" theme="success" variant="light"> 履行中 </t-tag>
          <t-tag v-if="row.status === CONTRACT_STATUS.FINISH" theme="success" variant="light"> 已完成 </t-tag>
        </template>
        <template #contractType="{ row }">
          <p v-if="row.contractType === CONTRACT_TYPES.MAIN">审核失败</p>
          <p v-if="row.contractType === CONTRACT_TYPES.SUB">待审核</p>
          <p v-if="row.contractType === CONTRACT_TYPES.SUPPLEMENT">待履行</p>
        </template>
        <template #paymentType="{ row }">
          <p v-if="row.paymentType === CONTRACT_PAYMENT_TYPES.PAYMENT" class="payment-col">
            付款<trend class="dashboard-item-trend" type="up" />
          </p>
          <p v-if="row.paymentType === CONTRACT_PAYMENT_TYPES.RECEIPT" class="payment-col">
            收款<trend class="dashboard-item-trend" type="down" />
          </p>
        </template>
        <template #op="slotProps">
          <a class="t-button-link" @click="rehandleClickOp(slotProps)">管理</a>
          <a class="t-button-link" @click="modify(slotProps)">修改</a>
          <a class="t-button-link" @click="handleClickDelete(slotProps)">删除</a>
        </template>
      </t-table>
      <t-dialog
        v-model:visible ="confirmVisible"
        header="确认删除当前所选合同？"
        :body="confirmBody"
        :on-cancel="onCancel"
        @confirm="onConfirmDelete"
      />

      <t-dialog v-model:visible="visible" header="基本信息" @confirm="onConfirm">
      <template #body>
        <div class="dialog-info-block">
          <div class="dialog-info-block">
            <div v-for="(item, index) in BASE_INFO_DATA" :key="index" class="info-item">
              <h1>{{ item.name }}</h1>
              <span
                :class="{
                  ['green']: item.type && item.type.value === 'green',
                  ['blue']: item.type && item.type.value === 'blue',
                }"
                >{{ item.value }}</span
              >
            </div>
          </div>
        </div>
      </template>
    </t-dialog>
    </div>
  </div>
</template>
<script setup lang="ts">
import { MessagePlugin, PageInfo, PrimaryTableCol, TableRowData } from 'tdesign-vue-next';
import { computed, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { getList, getOrderList } from '@/api/list';
import Trend from '@/components/trend/index.vue';
import { prefix } from '@/config/global';
import {
  CONTRACT_PAYMENT_TYPES,
  CONTRACT_STATUS,
  CONTRACT_STATUS_OPTIONS,
  CONTRACT_TYPE_OPTIONS,
  CONTRACT_TYPES,
} from '@/constants';
import { useSettingStore } from '@/store';

const BASE_INFO_DATA = ref([
  {
    name: '订单编号',
    value: 1,
    type: null,
  },
  {
    name: '客户编号',
    value: 1,
    type: {
      key: 'contractStatus',
      value: 'inProgress',
    },
  },
  {
    name: '产品编号',
    value: '1',
    type: null,
  },
  {
    name: '供应商编号',
    value: '1',
    type: null,
  },
  {
    name: '销售单价',
    value: '10000',
    type: null,
  },
  {
    name: '订购数量',
    value: '100',
    type: null,
  },
  {
    name: '订单金额',
    value: '100000',
    type: null,
  },
  {
    name: '预定时间',
    value: '欧尚',
    type: null,
  },
  {
    name: '订单时间',
    value: '2020-12-20',
    type: null,
  },
  {
    name: '备注',
    value: '2021-01-20',
    type: null,
  },
]);

const store = useSettingStore();
const router = useRouter();

const COLUMNS: PrimaryTableCol[] = [
  {
    title: '订单编号',
    fixed: 'left',
    width: 280,
    ellipsis: true,
    align: 'left',
    colKey: 'id',
  },
  { title: '客户编号', colKey: 'cid', width: 160 },
  {
    title: '产品编号',
    width: 160,
    ellipsis: true,
    colKey: 'pid',
  },
  {
    title: '供应商编号',
    width: 160,
    ellipsis: true,
    colKey: 'sid',
  },
  {
    title: '销售单价',
    width: 160,
    ellipsis: true,
    colKey: 'price',
  },
  {
    title: '订购数量',
    width: 160,
    ellipsis: true,
    colKey: 'amount',
  },
  {
    title: '订单金额',
    width: 160,
    ellipsis: true,
    colKey: 'money',
  },
  {
    title: '预定时间',
    width: 160,
    ellipsis: true,
    colKey: 'book_time',
  },
  {
    title: '订单时间',
    width: 160,
    ellipsis: true,
    colKey: 'order_time',
  },
  {
    title: '备注',
    width: 160,
    ellipsis: true,
    colKey: 'remark',
  },
  {
    align: 'left',
    fixed: 'right',
    width: 160,
    colKey: 'op',
    title: '操作',
  },
];

const searchForm = {
  name: '',
  no: '',
  status: typeof CONTRACT_STATUS,
  type: '',
};

const formData = ref({ ...searchForm });
const rowKey = 'index';
const verticalAlign = 'top' as const;
const hover = true;

const pagination = ref({
  defaultPageSize: 20,
  total: 100,
  defaultCurrent: 1,
});
const confirmVisible = ref(false);
const visible = ref(false);

const data = ref([]);

const dataLoading = ref(false);
const fetchData = async () => {
  dataLoading.value = true;
  try {
    const list = await getOrderList();
    // const { list } = await getList();
    console.log(list);
    data.value = list;
    console.log(data.value);
    pagination.value = {
      ...pagination.value,
      total: list.length,
    };
  } catch (e) {
    console.log(e);
  } finally {
    dataLoading.value = false;
  }
};

const deleteIdx = ref(-1);
const confirmBody = computed(() => {
  if (deleteIdx.value > -1) {
    const { name } = data.value[deleteIdx.value];
    return `删除后，${name}的所有合同信息将被清空，且无法恢复`;
  }
  return '';
});

const resetIdx = () => {
  deleteIdx.value = -1;
};

const onConfirmDelete = () => {
  // 真实业务请发起请求
  data.value.splice(deleteIdx.value, 1);
  pagination.value.total = data.value.length;
  confirmVisible.value = false;
  MessagePlugin.success('删除成功');
  resetIdx();
};

const onConfirm = () => {
  visible.value = false;
};

const modify = (ctx: unknown) => {
  console.log(ctx.row);
  router.push({ path: '/form/base', params: { info: ctx.row } });
};

const onCancel = () => {
  resetIdx();
};

onMounted(() => {
  fetchData();
});

const handleClickDelete = (slot: { row: { rowIndex: number } }) => {
  deleteIdx.value = slot.row.rowIndex;
  confirmVisible.value = true;
};
const onReset = (val: unknown) => {
  console.log(val);
};
const onSubmit = (val: unknown) => {
  console.log(val);
};
const rehandlePageChange = (pageInfo: PageInfo, newDataSource: TableRowData[]) => {
  console.log('分页变化', pageInfo, newDataSource);
};
const rehandleChange = (changeParams: unknown, triggerAndData: unknown) => {
  console.log('统一Change', changeParams, triggerAndData);
};
const rehandleClickOp = (ctx: unknown) => {
  visible.value = true;
  console.log(BASE_INFO_DATA.value);
  BASE_INFO_DATA.value = ctx.row;
  console.log(BASE_INFO_DATA.value);
  console.log(ctx.row.amount);
  BASE_INFO_DATA.value = [
    {
      name: '订单编号',
      value: ctx.row.id,
      type: null,
    },
    {
      name: '客户编号',
      value: ctx.row.cid,
      type: null,
    },
    {
      name: '产品编号',
      value: ctx.row.pid,
      type: null,
    },
    {
      name: '供应商编号',
      value: ctx.row.sid,
      type: null,
    },
    {
      name: '销售单价',
      value: ctx.row.price,
      type: null,
    },
    {
      name: '订购数量',
      value: ctx.row.amount,
      type: null,
    },
    {
      name: '订单金额',
      value: ctx.row.money,
      type: null,
    },
    {
      name: '预定时间',
      value: ctx.row.book_time,
      type: null,
    },
    {
      name: '订单时间',
      value: ctx.row.order_time,
      type: null,
    },
    {
      name: '备注',
      value: ctx.row.remark,
      type: null,
    },
  ];
};

const headerAffixedTop = computed(
  () =>
    ({
      offsetTop: store.isUseTabsRouter ? 48 : 0,
      container: `.${prefix}-layout`,
    } as any), // TO BE FIXED
);
</script>

<style lang="less" scoped>
.list-common-table {
  background-color: var(--td-bg-color-container);
  padding: var(--td-comp-paddingTB-xxl) var(--td-comp-paddingLR-xxl);
  border-radius: var(--td-radius-medium);

  .table-container {
    margin-top: var(--td-comp-margin-xxl);
  }
}

.form-item-content {
  width: 100%;
}

.operation-container {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  .expand {
    .t-button__text {
      display: flex;
      align-items: center;
    }
  }
}

.payment-col {
  display: flex;

  .trend-container {
    display: flex;
    align-items: center;
    margin-left: var(--td-comp-margin-s);
  }
}
</style>
