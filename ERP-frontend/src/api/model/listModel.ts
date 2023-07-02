export interface ListResult {
  list: Array<ListModel>;
}
export interface ListModel {
  adminName: string;
  amount: string;
  contractType: number;
  index: number;
  name: string;
  no: string;
  paymentType: number;
  status: number;
  updateTime: Date;
}

export interface CardListResult {
  list: Array<CardList>;
}
export interface CardList {
  banner: string;
  description: string;
  index: number;
  isSetup: boolean;
  name: string;
  type: number;
}

export interface Result {
  name: string;
  password: string;
}

export interface OrderListResult {
  list: Array<OrderModel>;
}
export interface OrderModel {
  data: {
    id: number;
    cid: number;
    pid: number;
    sid: number;
    price: number;
    amount: number;
    money: number;
    book_time: string;
    order_time: string;
    remark: string;
  };
}
