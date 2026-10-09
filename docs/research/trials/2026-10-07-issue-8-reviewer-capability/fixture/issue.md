# Preserve a clean slug for padded input

Input strings can contain leading or trailing spaces. These spaces currently produce leading or trailing hyphens. Strip surrounding whitespace before replacing inner spaces. Keep the existing lowercase behavior.

Success examples: ` Hello World ` becomes `hello-world`; `hello world` remains `hello-world`; whitespace-only input becomes an empty string.
