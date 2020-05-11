<template>
  <div class="layout-topbar">
    <button class="p-link layout-menu-button" @click="onMenuToggle">
      <span class="pi pi-bars"></span>
    </button>
    <div class="layout-topbar-icons">
      <a href="/product">
        <button class="p-link">
          <span class="layout-topbar-item-text">Product</span>
          <span class="layout-topbar-icon pi pi-calendar"></span>
        </button>
      </a>
      <a href="/order">
        <button class="p-link">
          <span class="layout-topbar-item-text">Order</span>
          <span class="layout-topbar-icon pi pi-calendar"></span>
        </button>
      </a>
      <a href="/work">
        <button class="p-link">
          <span class="layout-topbar-item-text">Work</span>
          <span class="layout-topbar-icon pi pi-calendar"></span>
        </button>
      </a>

      <span class="layout-topbar-search">
        <InputText type="text" placeholder="Search" />
        <span class="layout-topbar-search-icon pi pi-search"></span>
      </span>
      <button class="p-link">
        <span class="layout-topbar-item-text">Events</span>
        <span class="layout-topbar-icon pi pi-calendar"></span>
        <span class="layout-topbar-badge">5</span>
      </button>
      <button class="p-link">
        <span class="layout-topbar-item-text">Settings</span>
        <span class="layout-topbar-icon pi pi-cog"></span>
      </button>
      <button class="p-link">
        <span class="layout-topbar-item-text">User</span>
        <span class="layout-topbar-icon pi pi-user"></span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    onMenuToggle(event) {
      this.$emit("menu-toggle", event);
    }
  }
};
</script>