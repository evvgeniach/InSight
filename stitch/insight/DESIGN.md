---
name: InSight
colors:
  surface: '#fef9f1'
  surface-dim: '#ded9d2'
  surface-bright: '#fef9f1'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f8f3eb'
  surface-container: '#f2ede5'
  surface-container-high: '#ece8e0'
  surface-container-highest: '#e7e2da'
  on-surface: '#1d1c17'
  on-surface-variant: '#43474d'
  inverse-surface: '#32302b'
  inverse-on-surface: '#f5f0e8'
  outline: '#73777e'
  outline-variant: '#c3c7ce'
  surface-tint: '#416182'
  primary: '#416182'
  on-primary: '#ffffff'
  primary-container: '#7b9bbf'
  on-primary-container: '#0c3251'
  inverse-primary: '#a9c9ef'
  secondary: '#9c440f'
  on-secondary: '#ffffff'
  secondary-container: '#fd8e55'
  on-secondary-container: '#6e2a00'
  tertiary: '#615e58'
  on-tertiary: '#ffffff'
  tertiary-container: '#9c9891'
  on-tertiary-container: '#32302b'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d0e4ff'
  primary-fixed-dim: '#a9c9ef'
  on-primary-fixed: '#001d34'
  on-primary-fixed-variant: '#284969'
  secondary-fixed: '#ffdbcc'
  secondary-fixed-dim: '#ffb693'
  on-secondary-fixed: '#351000'
  on-secondary-fixed-variant: '#7a3000'
  tertiary-fixed: '#e7e2da'
  tertiary-fixed-dim: '#cac6be'
  on-tertiary-fixed: '#1d1b17'
  on-tertiary-fixed-variant: '#494741'
  background: '#fef9f1'
  on-background: '#1d1c17'
  surface-variant: '#e7e2da'
typography:
  display:
    fontFamily: Metropolis
    fontSize: 48px
    fontWeight: '600'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  h1:
    fontFamily: Metropolis
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  h2:
    fontFamily: Metropolis
    fontSize: 24px
    fontWeight: '500'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  h3:
    fontFamily: Metropolis
    fontSize: 20px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0em
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  data-tabular:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  xxl: 64px
  container-max: 1440px
  gutter: 24px
---

## Brand & Style

This design system establishes an "Editorial Analytical" aesthetic, moving away from the cold, clinical feel of traditional data tools toward a warmer, more intellectual environment. It prioritizes clarity and focus, utilizing generous white space and a sophisticated palette to reduce cognitive load during complex data synthesis.

The style is **Airy and Minimalist**, drawing inspiration from high-end print journalism. It balances the precision of data analysis with the comfort of a well-designed workspace. The interface should feel intentional, quiet, and premium, evoking a sense of calm authority for analysts and decision-makers.

## Colors

The palette is anchored by a **Professional Dusty Blue** used for primary actions and navigational cues, providing a trustworthy and stable foundation. The **Rich Terracotta** is reserved for the brand logo and critical "moment of insight" highlights, offering a warm, energetic contrast that draws the eye without causing fatigue.

The background uses a **Warm Beige** to soften the screen's glow, while **Soft Off-white** panels create a clear distinction for content areas. Borders are executed in a **Light Warm Gray**, ensuring structure is felt rather than seen, maintaining the airy, editorial feel.

## Typography

This system features a sophisticated typographic pairing to balance authority with utility. **Metropolis** is used for all headlines and display text, providing a geometric, modern, and high-end editorial feel. For all functional text, including body copy and labels, **Inter** is used to ensure maximum legibility and a systematic, utilitarian feel.

The hierarchy is strictly enforced to mimic editorial layouts: headers are bold and tightly spaced, while body copy is given ample line height for readability during long-form data interpretation. 

For data-heavy tables, use the `data-tabular` style which enables monospaced numeric features (tabular num) to ensure columns of figures align perfectly for visual scanning.

## Layout & Spacing

The layout philosophy follows a **fixed-fluid hybrid grid**. Main content areas are contained within a 1440px max-width wrapper to prevent line lengths from becoming unreadable on ultra-wide monitors. 

The spacing rhythm is built on an 8px base unit. To achieve the "airy" feel, use `xl (40px)` or `xxl (64px)` padding for page headers and section breaks. Sidebars should be fixed-width (280px) with fluid central panels that utilize a 12-column grid system for complex dashboard layouts.

## Elevation & Depth

Depth is conveyed through **Tonal Layers** and **Ambient Shadows**. The interface relies on the contrast between the Warm Beige background and Soft Off-white panels to establish hierarchy without heavy visual weight.

Shadows must be extremely subtle, using a soft blur and low opacity (3-5%) with a slight tint of the Dusty Blue to keep them feeling integrated rather than "dirty." 
- **Surface Level:** Flat on the Warm Beige.
- **Card Level:** 12px elevation with a light border (#E2DDD5) and a 4px blur shadow.
- **Active Level (Popovers/Modals):** 16px blur shadow to clearly separate the element from the data layer below.

## Shapes

The shape language combines softness with structure. A **12px radius** is applied to cards and panels to provide a welcoming, modern feel. Buttons and input fields use a slightly tighter **8px radius**, ensuring they feel like distinct, interactive components. 

Avoid fully pill-shaped elements for data inputs; stick to the 8px standard to maintain a professional, organized alignment.

## Components

### Buttons
Primary buttons use the Dusty Blue (#7B9BBF) with white text. Secondary buttons should use the Light Warm Gray border with no fill. For destructive actions, use a muted coral rather than a bright red to stay within the dusty palette.

### Input Fields
Inputs should have the Soft Off-white background and a 1px border (#E2DDD5). On focus, the border transitions to Dusty Blue with a 2px soft glow.

### Cards & Panels
Cards are the primary container for data visualizations. They must include 24px internal padding and 12px rounded corners. Headers within cards should use the `label-caps` style for metadata or `h3` (Metropolis) for titles.

### Data Visualizations
Charts should primarily use the Dusty Blue for the main data series. Use the Terracotta for "Current Trend" or "Target" lines to create immediate visual hierarchy. Background grid lines in charts should be kept at 0.5px thickness in Light Warm Gray.

### Chips & Filters
Filter chips should be rectangular with an 8px radius, utilizing the Warm Beige background to appear "pressed into" the surface until selected.