const routes = [
  {
    path: '/',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('src/pages/IndexPage.vue') }]
  },
  {
    path: '/p/:shortlink',
    component: () => import('src/layouts/ViewerLayout.vue'),
    children: [{ path: '', component: () => import('src/pages/PlanViewer.vue') }]
  },
  // {
  //   path: '/details/:shortlink',
  //   component: () => import('src/layouts/MainLayout.vue'),
  //   children: [
  //     { path: '', component: () => import('src/pages/PlanDetailPage.vue') }
  //   ]
  // },
  {
    path: '/edit/:planid',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/PlanInfoEditor.vue') }
    ]
  },
  {
    path: '/create',
    alias: ['/p/:shortlink/fork', '/edit/:planid/:planstateid/fork'],
    component: () => import('src/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/CreatePlanPage.vue') }
    ]
  },
  {
    path: '/edit/:planid/:planstateid',
    component: () => import('src/layouts/EditorLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/EditorCanvas.vue') }
    ]
  },
  {
    path: '/user/:userid',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/UserProfilePage.vue') }
    ]
  },
  {
    path: '/profile',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/MyProfilePage.vue') }
    ]
  },
  {
    path: '/privacy',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('src/pages/PrivacyPage.vue') }]
  },
  {
    path: '/liability',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/LiabilityPage.vue') }
    ]
  },
  {
    path: '/project',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/ProjectOverviewPage.vue') }
    ]
  },
  {
    path: '/impressum',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('src/pages/ImpressumPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
