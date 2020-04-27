import Vue from 'vue';
import Router from 'vue-router';
import Dashboard from './components/Dashboard.vue';

Vue.use(Router);

export default new Router({
	routes: [
		{
			path: "/login",
			name: "login",
			component: () => import("./pages/Login.vue")
		},
		{
			path: '/',
			name: 'dashboard',
			component: Dashboard
		},
		{
			path: '/merge',
			name: 'MergeDoc',
			component: () => import("./pages/MergeDoc.vue")
		},
		{
			path: '/search',
			name: 'SearchDoc',
			component: () => import("./pages/SearchDoc.vue")
		},
		{
			path: '/userManagement',
			name: 'UserManagement',
			component: ()=>import("./pages/UserManagement.vue")
		},
		{
			path: '/customer',
			name: 'Customer',
			component: ()=>import('./pages/Customer.vue'),
			children: [
				{
					path: ':id',
					name: 'CustomerDocument',
				}
			]
		},
		{
			path: '/product',
			name: "Product",
			component: ()=>import('./pages/Product.vue'),
			children: [
				{
					path: 'customer/:id',
					name: 'ProductCustomerList',
				},
				{
					path: ':id',
					name: 'ProductDocument',
				}
			]
		},
		{
			path: '/order',
			name: "Order",
			component: ()=>import('./pages/Order.vue'),
			children: [
				{
					path: 'customer/:id',
					name: 'OrderCustomerList',
				},
				{
					path: ':id',
					name: 'OrderDocument',
				}
			]
		},
		{
			path: '/work',
			name: "Work",
			component: ()=>import('./pages/Work.vue'),
			children: [
				{
					path: 'customer/:id',
					name: 'WorkCustomerList',
				},
				{
					path: ':id',
					name: 'WorkDocument',
				}
			]
		},
		{
			path: '/material',
			name: "Material",
			component: ()=>import('./pages/Material.vue'),
			children: [
				{
					path: 'customer/:id',
					name: 'MaterialCustomerList',
				},
				{
					path: ':id',
					name: 'MaterialDocument',
				}
			]
		},
		{
			path: '/empty',
			name: 'empty',
			component: () => import('./components/EmptyPage.vue')
		},
	],
	scrollBehavior() {
		return { x: 0, y: 0 };
	}
});