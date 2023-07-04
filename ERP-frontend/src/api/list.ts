import axios from 'axios';

import type { CardListResult, ListResult, OrderListResult } from '@/api/model/listModel';

import { request } from '@/utils/request';
const Api = {
  BaseList: '/get-list',
  CardList: '/get-card-list',
  OrderList: 'http://10.254.5.48:5000/api/order/',
  posturl: 'http://10.254.5.48:5000/api/manager/login/',
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
  axios({
    method: 'post',
    url: Api.posturl,
    params: {
      account,
      password,
    },
  }).then((res) => {
    console.log(res.data.status);
    return res.data.status;
  });
}

export async function getOrderList() {
  /* return request.get<OrderListResult>({
    url: Api.OrderList,
  }); */

  const response = await axios({
    method: 'get',
    url: Api.OrderList,
  }).then((res) => {
    // eslint-disable-next-line no-sequences
    return res.data.data;
  });
  console.log(response);
  return response;
}
