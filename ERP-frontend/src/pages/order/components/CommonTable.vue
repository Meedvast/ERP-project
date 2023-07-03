<template>
    <div class="list-common-table">
      <t-form ref="form" :data="formData" :label-width="80" colon @reset="onReset" @submit="onSubmit">
        <t-row>
          <t-col :span="10">
            <t-row :gutter="[24, 24]">
              <t-col :span="4">
                <t-form-item label="订单编号" name="name">
                  <t-input
                    v-model="formData.name"
                    class="form-item-content"
                    type="search"
                    placeholder="请输入订单编号"
                    :style="{ minWidth: '134px' }"
                  />
                </t-form-item>
              </t-col>
              <t-col :span="4">
                <t-form-item label="客户编号" name="name">
                  <t-input
                    v-model="formData.name"
                    class="form-item-content"
                    type="search"
                    placeholder="请输入客户编号"
                    :style="{ minWidth: '134px' }"
                  />
                </t-form-item>
              </t-col>
              <t-col :span="4">
                <t-form-item label="产品编号" name="name">
                  <t-input
                    v-model="formData.name"
                    class="form-item-content"
                    type="search"
                    placeholder="请输入产品编号"
                    :style="{ minWidth: '134px' }"
                  />
                </t-form-item>
              </t-col>
              <t-col :span="4">
                <t-form-item label="供应商编号" name="name">
                  <t-input
                    v-model="formData.name"
                    class="form-item-content"
                    type="search"
                    placeholder="请输入供应商编号"
                    :style="{ minWidth: '134px' }"
                  />
                </t-form-item>
              </t-col>
              <t-col :span="4">
                <t-form-item label="预订时间" name="name">
                  <t-input
                    v-model="formData.name"
                    class="form-item-content"
                    type="search"
                    placeholder="请输入预订时间"
                    :style="{ minWidth: '134px' }"
                  />
                </t-form-item>
              </t-col>
              <t-col :span="4">
                <t-form-item label="订单时间" name="name">
                  <t-input
                    v-model="formData.name"
                    class="form-item-content"
                    type="search"
                    placeholder="请输入订单"
                    :style="{ minWidth: '134px' }"
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
            <a class="t-button-link" @click="handleClickDelete(slotProps)">删除</a>
          </template>
        </t-table>
        <t-dialog
          v-model:visible="confirmVisible"
          header="确认删除当前所选合同？"
          :body="confirmBody"
          :on-cancel="onCancel"
          @confirm="onConfirmDelete"
        />
      </div>
    </div>
  </template>
  <script setup lang="ts">
  import { MessagePlugin, PageInfo, PrimaryTableCol, TableRowData } from 'tdesign-vue-next';
  import { computed, onMounted, ref } from 'vue';
  
  import { getList } from '@/api/list';
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
  
  const store = useSettingStore();
  
  const COLUMNS: PrimaryTableCol[] = [
    {
      title: '订单编号',
      width: 160,
      ellipsis: true,
      colKey: 'no',
    },
    {
      title: '客户编号',
      width: 160,
      ellipsis: true,
      colKey: 'no',
    },
    {
      title: '产品编号',
      width: 160,
      ellipsis: true,
      colKey: 'no',
    },
    {
      title: '供应商编号',
      width: 160,
      ellipsis: true,
      colKey: 'no',
    },
    {
      title: '销售单价',
      width: 160,
      ellipsis: true,
      colKey: 'no',
    },
    {
      title: '订购数量',
      width: 160,
      ellipsis: true,
      colKey: 'no',
    },
    {
      title: '订购金额',
      width: 160,
      ellipsis: true,
      colKey: 'no',
    },
    {
      title: '预订时间',
      width: 160,
      ellipsis: true,
      colKey: 'no',
    },
    {
      title: '订单时间',
      width: 160,
      ellipsis: true,
      colKey: 'no',
    },
    {
      title: '备注册表',
      width: 160,
      ellipsis: true,
      colKey: 'no',
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
  
  const data = ref([]);
  
  const dataLoading = ref(false);
  const fetchData = async () => {
    dataLoading.value = true;
    try {
      const { list } = await getList();
      data.value = list;
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
    console.log(ctx);
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
  