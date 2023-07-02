import type { CardListResult, ListResult, OrderListResult } from '@/api/model/listModel';
import { request } from '@/utils/request';

const Api = {
  BaseList: '/get-list',
  CardList: '/get-card-list',
  OrderList: '172.16.1.11:5000/api/order/',
  posturl: '172.16.1.11:5000/api/manager/login/',
};

export function getList() {
  return request.get<ListResult>({
    url: Api.BaseList,
  });
}

export function getCardList() {
  return request.get<CardListResult>({
    url: Api.CardList,
  });
}

export function getUserInfo(account: string, password: string) {
  return request.post({
    url: Api.posturl,
    data: {
      account,
      password,
    },
  });
}

export function getOrderList() {
  return request.get<OrderListResult>({
    url: Api.OrderList,
  });
}
