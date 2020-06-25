import Vue from 'vue';
import Router from 'vue-router';
import Dashboard from '@/prime/components/Dashboard.vue';

Vue.use(Router);

export default new Router({
	
    mode: 'history',

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
			component: () => import("./pages/UserManagement.vue")
		},

		/// customer
		{
			path: '/customer',
			name: 'Customer',
			component: () => import('./pages/Customer.vue'),
		},
		{
			path: '/customer/:id',
			name: 'Customer Details',
			component: () => import('./pages/Customer.vue'),
		},

		//product
		{
			path: '/product',
			name: "Product",
			component: () => import('./pages/Product.vue'),
		},
		{
			path: '/product/customer/:id',
			name: "Product By Customer",
			component: () => import('./pages/Product.vue'),
		},

		{
			path: '/product/:id',
			name: 'Product Details',
			component: () => import('./pages/ProductDocument.vue'),
		},

		////order
		{
			path: '/order',
			name: "Order",
			component: () => import('./pages/Order.vue'),
			children: [
				{
					path: 'customer/:id',
					name: 'OrderCustomerList',
				}
			]
		},
		{
			path: '/order/:id',
			name: 'Order Details',
			component: () => import('./pages/OrderDocument.vue'),
		},
		/// work paths and children
		{
			path: '/work',
			name: "Work",
			component: () => import('./pages/Work.vue'),
			children: [
				{
					path: 'customer/:id',
					name: 'WorkCustomerList',
				},
			]
		},
		{
			path: '/work/:id',
			name: 'WorkDocument',
			component: () => import('./pages/WorkDocument.vue'),

		},

		{
			path: '/material',
			name: "Material",
			component: () => import('./pages/Material.vue'),
		},
		{
			path: '/material/:id',
			name: "Material Deatils",
			component: () => import('./pages/MaterialDocument.vue'),
		},

		///prime vue paths
		{
			path: '/sample',
			name: 'sample',
			component: () => import('@/prime/components/SampleDemo.vue')
		},
		{
			path: '/forms',
			name: 'forms',
			component: () => import('@/prime/components/FormsDemo.vue')
		},
		{
			path: '/data',
			name: 'data',
			component: () => import('@/prime/components/DataDemo.vue')
		},
		{
			path: '/panels',
			name: 'panels',
			component: () => import('@/prime/components/PanelsDemo.vue')
		},
		{
			path: '/overlays',
			name: 'overlays',
			component: () => import('@/prime/components/OverlaysDemo.vue')
		},
		{
			path: '/menus',
			component: () => import('@/prime/components/MenusDemo.vue'),
			children: [{
				path: '',
				component: () => import('@/prime/components/menu/PersonalDemo.vue')
			},
			{
				path: '/menus/seat',
				component: () => import('@/prime/components/menu/SeatDemo.vue')
			},
			{
				path: '/menus/payment',
				component: () => import('@/prime/components/menu/PaymentDemo.vue')
			},
			{
				path: '/menus/confirmation',
				component: () => import('@/prime/components/menu/ConfirmationDemo.vue')
			}]
		},
		{
			path: '/messages',
			name: 'messages',
			component: () => import('@/prime/components/MessagesDemo.vue')
		},
		{
			path: '/charts',
			name: 'charts',
			component: () => import('@/prime/components/ChartsDemo.vue')
		},
		{
			path: '/misc',
			name: 'misc',
			component: () => import('@/prime/components/MiscDemo.vue')
		},
		// {
		// 	path: '/empty',
		// 	name: 'empty',
		// 	component: () => import('@/prime/components/EmptyPage.vue')
		// },
		// {
		// 	path: '/documentation',
		// 	name: 'documentation',
		// 	component: () => import('@/prime/components/Documentation.vue')
		// },
	],
	scrollBehavior() {
		return { x: 0, y: 0 };
	}
});