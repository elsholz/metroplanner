
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },
  {
    path: '/p/:shortlink',
    component: () => import('src/layouts/ViewerLayout.vue'),
    children: [
      { path: '', component: () => import('pages/PlanViewer.vue') }
    ]
  },
  {
    path: '/edit/:planid',
    component: () => import('src/layouts/EditorLayout.vue'),
    children: [
      { path: '', component: () => import('pages/PlanEditor.vue') }
    ]
  },
  {
    path: '/privacy',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/PrivacyPage.vue') }
    ]
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
