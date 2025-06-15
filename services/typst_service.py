import typst

def main():
    # Compile `hello.typ` to PDF and save as `hello.pdf`
    typst.compile(
        input=r"D:\Projects\Professional Portfolio Project\cv_gen_BE\templates\typst_ramindu.typ",
        output=r"D:\Projects\Professional Portfolio Project\cv_gen_BE\templates\typst_ramindu.pdf"
    )

    # Or use Compiler class to avoid reinitialization
    # compiler = typst.Compiler("hello.typ")
    # compiler.compile(format="png", ppi=144.0)

if __name__ == "__main__":
    main()