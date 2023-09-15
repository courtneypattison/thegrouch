import { useEffect, useState } from 'react';

export default function Categories() {
  const reactPort = '5173';
  const apiPort = '8000';
  const host = 'http://localhost:';
  const [categories, setCategories] = useState([]);

  function fetchCategories() {
    fetch('/api/categories')
    .then(response => response.json())
    .then(json => setCategories(json));
  }

  useEffect(() => {
    fetchCategories();
  }, []);

  return (
    <div className='mx-auto max-w-7xl px-4 sm:px-6 lg:px-8'>
      <div className='mx-auto max-w-2xl py-16 sm:py-24 lg:max-w-none lg:py-32'>
        <h1 className="text-2xl font-bold">Shop by Category</h1>
        <div className="mt-6 space-y-12 lg:grid lg:grid-cols-3 lg:gap-x-6 lg:space-y-0">
          {categories.map(c => {
            return (
              <a
                className='group relative'
                href={host + apiPort + '/catalogue/category/' + c.slug + '_' + c.url.split('/').at(-2)}
                key={c.url}
              >
                <figure>
                  <img
                    className="relative h-80 w-full overflow-hidden rounded-lg bg-white sm:aspect-h-1 sm:aspect-w-2 lg:aspect-h-1 lg:aspect-w-1 group-hover:opacity-75 sm:h-64"
                    src={c.image.replace(reactPort, apiPort)}
                  />
                  <figcaption className="text-gray-500 text-sm">{c.name}</figcaption>
                </figure>
                <p className='font-semibold'>{c.description.replace(/^<p>/, "").replace(/<\/p>$/, "")}</p>
              </a>
            );
          })}
        </div>
      </div>
    </div>
  );
}