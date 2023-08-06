if __name__ == "__main__":
    from crdatamgt import runner
    import warnings

    warnings.simplefilter(action="ignore", category=FutureWarning)
    runner.process_data()
