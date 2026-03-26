<template>
  <UApp>
    <NuxtPage />
  </UApp>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap");

body {
  font-family: "Plus Jakarta Sans", sans-serif;
  background-color: #f8fafc;
  color: #1e293b;
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

* {
  box-sizing: border-box;
}

.btn-primary {
  background: #2563eb;
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
  text-decoration: none;
  display: inline-block;
}

.btn-primary:hover {
  background: #1d4ed8;
}
</style>
