<template>
  <header class="border-b py-3.5 flex items-center mb-14">
    <div class="container mx-auto px-4 xl:px-0 flex justify-between items-center">
      <div class="flex space-x-4 items-center">
        <img src="/logo.png" width="28" height="28" alt="Malaysia Inflation Calculator">
        <p class="text-xl hidden md:inline-block">Malaysia Inflation Calculator</p>
      </div>
      <div class="flex space-x-4 items-center">
        <!-- icon github, fontawesome -->
        <a href="https://github.com/xkre/malaysia-inflation-calc" target="_blank">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" color="currentColor" viewBox="0 0 496 512"><!--! Font Awesome Pro 6.2.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path d="M165.9 397.4c0 2-2.3 3.6-5.2 3.6-3.3.3-5.6-1.3-5.6-3.6 0-2 2.3-3.6 5.2-3.6 3-.3 5.6 1.3 5.6 3.6zm-31.1-4.5c-.7 2 1.3 4.3 4.3 4.9 2.6 1 5.6 0 6.2-2s-1.3-4.3-4.3-5.2c-2.6-.7-5.5.3-6.2 2.3zm44.2-1.7c-2.9.7-4.9 2.6-4.6 4.9.3 2 2.9 3.3 5.9 2.6 2.9-.7 4.9-2.6 4.6-4.6-.3-1.9-3-3.2-5.9-2.9zM244.8 8C106.1 8 0 113.3 0 252c0 110.9 69.8 205.8 169.5 239.2 12.8 2.3 17.3-5.6 17.3-12.1 0-6.2-.3-40.4-.3-61.4 0 0-70 15-84.7-29.8 0 0-11.4-29.1-27.8-36.6 0 0-22.9-15.7 1.6-15.4 0 0 24.9 2 38.6 25.8 21.9 38.6 58.6 27.5 72.9 20.9 2.3-16 8.8-27.1 16-33.7-55.9-6.2-112.3-14.3-112.3-110.5 0-27.5 7.6-41.3 23.6-58.9-2.6-6.5-11.1-33.3 2.6-67.9 20.9-6.5 69 27 69 27 20-5.6 41.5-8.5 62.8-8.5s42.8 2.9 62.8 8.5c0 0 48.1-33.6 69-27 13.7 34.7 5.2 61.4 2.6 67.9 16 17.7 25.8 31.5 25.8 58.9 0 96.5-58.9 104.2-114.8 110.5 9.2 7.9 17 22.9 17 46.4 0 33.7-.3 75.4-.3 83.6 0 6.5 4.6 14.4 17.3 12.1C428.2 457.8 496 362.9 496 252 496 113.3 383.5 8 244.8 8zM97.2 352.9c-1.3 1-1 3.3.7 5.2 1.6 1.6 3.9 2.3 5.2 1 1.3-1 1-3.3-.7-5.2-1.6-1.6-3.9-2.3-5.2-1zm-10.8-8.1c-.7 1.3.3 2.9 2.3 3.9 1.6 1 3.6.7 4.3-.7.7-1.3-.3-2.9-2.3-3.9-2-.6-3.6-.3-4.3.7zm32.4 35.6c-1.6 1.3-1 4.3 1.3 6.2 2.3 2.3 5.2 2.6 6.5 1 1.3-1.3.7-4.3-1.3-6.2-2.2-2.3-5.2-2.6-6.5-1zm-11.4-14.7c-1.6 1-1.6 3.6 0 5.9 1.6 2.3 4.3 3.3 5.6 2.3 1.6-1.3 1.6-3.9 0-6.2-1.4-2.3-4-3.3-5.6-2z"/></svg>
        </a>

        <div class="flex">
          <!-- icon sun-high -->
          <button class="border py-1 px-3 rounded-l-md hover:border-blue-500 hover:bg-blue-50 border-blue-500 bg-blue-50 text-blue-500">
            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-sun-high" width="20" height="20" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path d="M14.828 14.828a4 4 0 1 0 -5.656 -5.656a4 4 0 0 0 5.656 5.656z"></path>
              <path d="M6.343 17.657l-1.414 1.414"></path>
              <path d="M6.343 6.343l-1.414 -1.414"></path>
              <path d="M17.657 6.343l1.414 -1.414"></path>
              <path d="M17.657 17.657l1.414 1.414"></path>
              <path d="M4 12h-2"></path>
              <path d="M12 4v-2"></path>
              <path d="M20 12h2"></path>
              <path d="M12 20v2"></path>
            </svg>
          </button>
          <button class="border py-1 px-3 rounded-r-md hover:border-blue-500 hover:bg-blue-50 -ml-px">
          <!-- icon moon-stars -->
            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-moon-stars" width="20" height="20" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path d="M12 3c.132 0 .263 0 .393 0a7.5 7.5 0 0 0 7.92 12.446a9 9 0 1 1 -8.313 -12.454z"></path>
              <path d="M17 4a2 2 0 0 0 2 2a2 2 0 0 0 -2 2a2 2 0 0 0 -2 -2a2 2 0 0 0 2 -2"></path>
              <path d="M19 11h2m-1 -1v2"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </header>

  <section class="max-w-screen-sm mx-auto px-4 md:px-0 mb-8">
    <img src="/logo.png" width="40" height="40" alt="Malaysia Inflation Calculator" class="mb-7">
    <h1 class="text-3xl md:text-5xl mb-4">Malaysia Inflation Calculator</h1>
    <p class="text-lg">A simple calculator that calculates the equivalent purchasing power between two time periods. Use official published data from Department of Statistics, Malaysia and other third party sources for the misc data such as Big Mac Index.</p>
  </section>
</template>