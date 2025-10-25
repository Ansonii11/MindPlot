// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'My Docs',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/withastro/starlight' }],
			customCss: [
				'./src/styles/custom.css',
			],
			sidebar: [
				{
					label: 'Fundamentos de interpretación',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: 'Correlación vs Casualidad', slug: 'fundamentos/correlacion' },
						{ label: 'Tendencia vs Ruido', slug: 'fundamentos/tendencia' },
					],
				},
			],
		}),
	],
});
