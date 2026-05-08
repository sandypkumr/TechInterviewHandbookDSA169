import { defineCollection, z } from 'astro:content';

const problems = defineCollection({
  type: 'content',
  schema: z.object({
    title:             z.string(),
    problemSlug:       z.string(),
    topic:             z.string(),
    topicSlug:         z.string(),
    difficulty:        z.enum(['Easy', 'Medium', 'Hard']),
    leetcodeUrl:       z.string().url(),
    githubUrl:         z.string().url(),
    tags:              z.array(z.string()).default([]),
    patterns:          z.array(z.string()).default([]),
    timeComplexity:    z.string().optional(),
    spaceComplexity:   z.string().optional(),
    hasProblemStatement: z.boolean().default(false),
    hasConstraints:    z.boolean().default(false),
    hasExamples:       z.boolean().default(false),
    isPremium:         z.boolean().default(false),
    similarProblems:   z.array(z.string()).default([]),
  }),
});

const topics = defineCollection({
  type: 'content',
  schema: z.object({
    title:        z.string(),
    description:  z.string().optional(),
    icon:         z.string().optional(),
    problemCount: z.number().default(0),
    easyCount:    z.number().default(0),
    mediumCount:  z.number().default(0),
    hardCount:    z.number().default(0),
    patterns:     z.array(z.string()).default([]),
    order:        z.number().default(99),
  }),
});

const cheatsheets = defineCollection({
  type: 'content',
  schema: z.object({
    title:       z.string(),
    description: z.string(),
    category:    z.string(),
    order:       z.number().default(0),
    tags:        z.array(z.string()).default([]),
  }),
});

export const collections = { problems, topics, cheatsheets };
