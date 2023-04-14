const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/IndexPage.vue') }]
  },
  {
    path: '/p/:shortlink',
    component: () => import('src/layouts/ViewerLayout.vue'),
    children: [{ path: '', component: () => import('pages/PlanViewer.vue') }]
  },
  {
    path: '/details/:shortlink',
    component: () => import('src/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/PlanDetailPage.vue') }
    ]
  },
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
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/UserProfilePage.vue') }
    ]
  },
  {
    path: '/profile',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/MyProfilePage.vue') }
    ]
  },
  {
    path: '/privacy',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/PrivacyPage.vue') }]
  },
  {
    path: '/liability',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/LiabilityPage.vue') }
    ]
  },
  {
    path: '/project',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/ProjectOverviewPage.vue') }
    ]
  },
  {
    path: '/impressum',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/ImpressumPage.vue') }
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
