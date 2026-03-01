import argparse
from pathlib import Path
import sys
from .models.config import ConverterConfig
from .core.converter import HDXConverter

def main():
    parser = argparse.ArgumentParser(
        description='Convert HDX documentation to multiple formats with metadata',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m hdx_converter input.hdx
  python -m hdx_converter input.hdx -o output_dir --max-articles 100
  python -m hdx_converter input.hdx --skip-extract --no-md
        """
    )
    
    # Основные аргументы
    parser.add_argument('hdx_file', type=Path,
                       help='Path to HDX file')
    parser.add_argument('-o', '--output', type=Path, default=Path('hdx_output'),
                       help='Output directory (default: hdx_output)')
    
    # Настройки обработки
    parser.add_argument('-n', '--max-articles', type=int,
                       help='Process only first N articles')
    parser.add_argument('--skip-extract', action='store_true',
                       help='Skip HDX extraction and use existing HTML backup files')
    
    # Настройки форматов вывода
    parser.add_argument('--no-md', action='store_true',
                       help='Skip Markdown generation')
    parser.add_argument('--no-txt', action='store_true',
                       help='Skip text file generation')
    parser.add_argument('--no-json', action='store_true',
                       help='Skip JSON metadata generation')
    parser.add_argument('--no-images', action='store_true',
                       help='Skip image copying')
    parser.add_argument('--no-backup', action='store_true',
                       help='Skip HTML backup')
    
    # Настройки логирования
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose logging (DEBUG level)')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Enable quiet mode (WARNING level only)')
    
    # Настройки валидации
    parser.add_argument('--no-validate', action='store_true',
                       help='Skip metadata validation')
    parser.add_argument('--no-stats', action='store_true',
                       help='Skip statistics collection and display')
    
    args = parser.parse_args()
    
    # Проверка входного файла
    if not args.hdx_file.exists() and not args.skip_extract:
        print(f"Error: HDX file '{args.hdx_file}' not found")
        sys.exit(1)
    
    # Проверка наличия tqdm для прогресс-бара
    try:
        import tqdm
        HAS_TQDM = True
    except ImportError:
        HAS_TQDM = False
        print("Note: tqdm not installed. Progress bars will be disabled.")
        print("Install with: pip install tqdm")
    
    # Настройка уровня логирования
    log_level = "INFO"
    if args.verbose:
        log_level = "DEBUG"
    elif args.quiet:
        log_level = "WARNING"
    
    # Создание конфигурации
    config = ConverterConfig(
        output_dir=args.output,
        max_articles=args.max_articles,
        skip_extract=args.skip_extract,
        generate_markdown=not args.no_md,
        generate_text=not args.no_txt,
        generate_json_metadata=not args.no_json,
        copy_images=not args.no_images,
        backup_html=not args.no_backup,
        validate_metadata=not args.no_validate,
        collect_statistics=not args.no_stats,
        print_statistics=not args.no_stats,
        log_level=log_level
    )
    
    # Создание и запуск конвертера
    try:
        converter = HDXConverter(config)
        converter.convert(args.hdx_file)
    except KeyboardInterrupt:
        print("\nConversion interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()